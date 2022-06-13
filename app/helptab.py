from app import secrets
# Internal function to scrape "areas" from game helptab file
#
# The "areas" are each listed in the "helptab" file on lines starting with "32 Area " ...
# ...followed by descriptions until the character "#" on a single line itself
def _get_help_area(area=None):

    # Get game "helptab" file path/name, and open it
    helptab_file = secrets.helptab_file
    helptab_fh = open(helptab_file, 'r')

    # Prepare an empty "areas" dictionary
    areas = {}

    # Do not keep lines by default
    keep = False

    # Loop through each line, finding and keeping chunks staring with "32 Area "
    for line in helptab_fh:
        stripped = line.strip()

        # Stop line (#)
        if keep == True and stripped == '#':
            keep = False

        # Do not include "other levels" info (%%)
        if keep == True and stripped.startswith('%% '):
            keep = False

        # Append the current chunk to our areas dictionary, under the key of whatever started with "32 Area " last
        if keep == True and not stripped.startswith('32 Area '):
            areas[area_name] += line

        # Start new dictionary keys of chunks at lines beginning with "32 Area "
        if stripped.startswith('32 Area '):
            keep = True
            area_name = stripped.replace('32 Area ', '')
            areas[area_name] = ''

    # Close the "helptab" file
    helptab_fh.close()

    # Return either the single area, or a list of them
    if area != None and areas[area]:
        return areas[area]
    elif areas != None and len(areas) > 0:
        return areas
    else:
        return None
