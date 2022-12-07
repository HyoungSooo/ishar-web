"""Parse the MUD 'helptab' file"""
import re
from flask import url_for
from mud_secret import HELPTAB, IMM_LEVELS
from sentry import sentry_sdk

# Compile a few regular expressions for use later
#   to parse out specific items from help topic chunks
see_also_regex = re.compile(r'^ *(see also|also see|also see help on|see help on|related) *\:*', re.IGNORECASE)
regexes = {
    'syntax':   re.compile(r'^ *(Syntax|syntax) *\: *(.+)$'),
    'minimum':  re.compile(r'^ *(Minimum|minimum|Min|min) *\: *(.+)$'),
    'level':    re.compile(r'^ *(Level|level) *\: *(.+)$'),
    'class':    re.compile(r'^ *(Class|Classes) *\: *(.+)$'),
    'save':     re.compile(r'^ *(Saves?) *\: *(.+)$')
}

def get_help_chunks(help_file=HELPTAB):
    """Parse the MUD 'helptab' file into chunks, by '#' character, to roughly separate topics"""

    # Open the 'helptab' file (read-only)
    try:
        with open(file=help_file, mode='r', encoding='utf-8') as help_fh:

            # Split the contents of the file into a list,
            #   where each item is separated by "\n#\n" - hash (#) on a line by itself
            #   and return "chunks" except the first (instructions/example)
            return help_fh.read().split('\n#\n')[1:]

    # Catch/return exceptions or errors on accessing the 'helptab' file,
    #   and report to Sentry
    except (FileNotFoundError, PermissionError, Exception) as err:
        sentry_sdk.capture_exception(err)
        return []

    # Close the 'helptab' file
    finally:
        help_fh.close()


def get_help_topics():
    """Parse the MUD 'helptab' file chunked list into dictionry of topics"""

    # Get helptab file list of chunks
    help_chunks = get_help_chunks()
    help_topics = {}

    # Loop through each chunk from the list
    for help_chunk in help_chunks:

        # Parse the chunk from the list
        parsed_chunk = parse_help_chunk(help_chunk=help_chunk)

        # If the chunk was parsed, and named, add it to a dictionary of topics to return
        if parsed_chunk and 'name' in parsed_chunk:
            parsed_name = parsed_chunk['name']
            help_topics[parsed_name] = parsed_chunk

    # Return a dictionary of topics, parsed from the list of chunks
    return help_topics


def parse_help_chunk(help_chunk=None):
    """Parse a single chunk from the MUD 'helptab' file into a help topic"""

    # Split the chunk in half on the separator, between its header and body text:
    #   "\n*\n" - asterisk (*), on a line by itself
    halves = help_chunk.split('\n*\n')
    help_topic = {}

    # Proceed if there are two halves
    if len(halves) == 2:

        # Parse the help topic header, which is everything before '*'
        help_header = parse_help_header(header=halves[0])

        # Proceed if mortals should be able to reach the topic,
        #   and it starts with "32 "
        if help_header and 'name' in help_header:
            help_content = halves[1].replace('>', '&gt;').replace('<', '&lt;').replace('"', '&quot;')
            help_topic = parse_help_content(content=help_content)
            help_topic['name'] = help_header['name']
            help_topic['aliases'] = help_header['aliases']

    # Return the help topic dictionary
    return help_topic


def parse_help_body(line=None):
    """Parse the body from a single topic chunk from the MUD 'helptab' file
        for specific item regular expression values"""
    for iname, regex in regexes.items():
        find = regex.findall(line)
        if find:
            return {iname: find[0][1]}
    return line


def parse_help_content(content=None):
    """Parse the body content from a single topic chunk from the MUD 'helptab' file
        to return a help topic dictionary"""

    # Topic body text is everything after the header and '*',
    #   but replace < and > and " with HTML-safe versions

    # Loop through each line of the help chunk body text
    is_see_also = False
    help_topic = {}
    help_topic['body_text'] = str()
    for line in content.split('\n'):

        if see_also_regex.match(line):
            help_topic['body_text'] += 'See Also: '
            is_see_also = True

        if is_see_also:
            rmbegin = line.split(':')
            related_topics = rmbegin[-1].strip().split(',')

            # Append each related topic to our list to return
            i = 0
            num_related = len(related_topics)
            for related_topic in related_topics:
                i += 1
                if related_topic and related_topic.strip() != '':
                    related_link = f"<a href=\"{url_for('help_page.single', topic=related_topic.strip())}\">{related_topic.strip()}</a>"
                    help_topic['body_text'] += related_link
                    if i != num_related:
                        help_topic['body_text'] += ', '
                    else:
                        is_see_also = False

        else:
            # Parse the body line
            parsed_line = parse_help_body(line=line)

            # Append strings to the body text
            if isinstance(parsed_line, str):
                help_topic['body_text'] += f'{line}\n'

            # Set dictionary values from regex matches
            if isinstance(parsed_line, dict):
                for item_name, item_value in parsed_line.items():
                    help_topic[item_name] = item_value

    # Replace "`help command'" in the body text with link to that help command
    cmd_pattern = r"`help ([\w| ]+)'"
    help_topic['body_text'] = re.sub(cmd_pattern, r'`<a href="/help/\1">help \1</a>`', help_topic['body_text'], re.MULTILINE)

    return help_topic


def parse_help_header(header=None):
    """Parse the header from a single topic chunk from the MUD 'helptab' file"""

    # The 'for_level' of the help topic is a number alone, on the first line of the header
    help_header = {}
    header_lines = header.split('\n')
    help_header['for_level'] = int(header_lines[0].strip())

    # Name the topic if mortals should be able reach it, and it starts with "32 "
    if help_header['for_level'] < min(IMM_LEVELS) and header_lines[1].startswith('32 '):
        help_header['name'] = header_lines[1].replace('32 ', '').strip()
        help_header['aliases'] = []

        # Loop through each line of the header
        for header_line in header_lines:

            # Any lines starting with '32 ' are potential names/aliases
            if header_line.startswith('32 '):

                # Set any aliases, which are not the primary name
                header_line_clean = header_line.replace('32 ', '').strip()
                if header_line_clean != help_header['name']:
                    help_header['aliases'].append(header_line_clean)

    # Return the help topic header
    return help_header


def search_help_topics(all_topics=None, search=None):
    """Search all help topics for a specific topic name or alias"""

    # Get all help topics, if necessary
    if not all_topics:
        all_topics = get_help_topics()

    # If there is no search, return all help topics
    if search is None:
        help_topics = all_topics

    # Loop through each topic to find any matches in the names or aliases
    else:
        help_topics = {}
        search = search.lower()
        for tname, tvals in all_topics.items():

            # Return exact name matches immediately
            if search == tname.lower():
                return { tname: tvals }

            # Add partial name matches
            if search in tname.lower():
                help_topics[tname] = tvals

            # If there was no name match, check aliases
            else:

                # Loop through each alias
                for topic_alias in tvals['aliases']:

                    # Return exact alias matches immediately
                    if search == topic_alias.lower():
                        return { topic_alias: tvals }

                    # Add partial alias matches
                    if search in topic_alias.lower():
                        help_topics[topic_alias] = tvals

    # Return any partial matches
    return help_topics
