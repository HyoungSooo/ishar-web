#!/usr/bin/python3
"""Ishar MUD Discord bot"""
from datetime import datetime

import logging
import re
import signal
import sys

import interactions

from config import DISCORD
from database import db_session
from help.helptab import search_help_topics

import models

from sentry import sentry_sdk
from sysinfo import get_connections, get_uptime


# Create/compile a regular expression to only match letters,
#   for command arguments
regex = re.compile(r'^[a-z A-Z]+$')

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S %Z'
)

# Connect/authenticate Ishar MUD Discord bot
bot = interactions.Client(
    token=DISCORD['TOKEN'],
    default_scope=DISCORD['GUILD']
)


# Method to get the details of a single help topic
def get_single_help(topic=None):
    """Return extended output for a single help topic"""

    # Get the single topic name and link
    url = f"<https://isharmud.com/help/{topic['name']}>".replace(' ', '%20')
    out = f"{topic['name']}: {url}\n"

    # Get any specific items within the help topic
    for item_type in ['syntax', 'minimum', 'class', 'level']:
        if item_type in topic:
            if topic[item_type].strip() != '':
                out += f'> {item_type.title()}: '
                out += f'{topic[item_type].strip()}\n'

    # Only return the name/link and specific items, if the body is too big
    out_wbody = f"{out}```{topic['body_text']}```"
    if len(out_wbody) > 2000:
        return out

    # Otherwise, return the whole body
    return out_wbody


# /challenges <search?>
@bot.command(
    name='challenges',
    description='Find Ishar MUD challenge(s)',
    options=[
        interactions.Option(
            name='search',
            description='name of a mob to search challenges',
            type=interactions.OptionType.STRING,
            required=False
        )
    ]
)
async def challenges(
    ctx: interactions.CommandContext,
    search: str = None
):
    """Show the current active Ishar MUD challenges"""
    ephemeral = True
    find = None
    out = None
    logging.info(
        '%s (%i) / %s / challenges',
        ctx.channel, ctx.channel_id, ctx.user
    )

    # Handle search (for challenge mob name)
    if search:

        # Make sure that the search term is only letters
        if not regex.match(search):
            out = 'Sorry, but please stick to letters!'

        else:
            find = models.Challenge.query.filter_by(
                is_active=1
            ).filter(
                models.Challenge.mob_name.like(
                    '%' + search + '%'
                )
            ).all()

            if not find:
                out = 'Sorry, but no challenges could be found!'

    if not out:

        # Find all active challenges by default
        if not find:
            find = models.Challenge.query.filter_by(is_active=1).all()

        out = '**Challenges**\n'
        i = completed = 0
        for challenge in find:

            # Strikethrough, and count, completed mobs
            i += 1
            mob_name = challenge.mob_name
            if challenge.is_completed:
                completed += 1
                mob_name = f'~~{challenge.mob_name}~~'

            out += f'{i}: {mob_name} / '
            out += f'{challenge.adj_people} people / '
            out += f'Level: {challenge.adj_level} / '
            out += f'Tier: {challenge.display_tier} '

            if challenge.is_completed:
                out += f' / Completed by: {challenge.winner_desc}'

            out += '\n'

        out += f'*{completed}* completed out of *{len(find)}* found!\n'

    # Send the challenges response
    await ctx.send(
        out,
        ephemeral=ephemeral
    )
    db_session.close()


# /deadhead
@bot.command()
async def deadhead(ctx: interactions.CommandContext):
    """Show the player with the most in-game deaths"""
    logging.info(
        '%s (%i) / %s / deadhead',
        ctx.channel, ctx.channel_id, ctx.user
    )

    # Find player with the most deaths
    deadman = ''
    deadman.name = 'WIP'
    deadman.deaths = 0
    """Player.query.filter_by(
        is_deleted=0, game_type=0
    ).order_by(-Player.deaths).first()"""

    # Show the name and death count of the player with the most deaths
    out = 'The player who has died most is: '
    out += f'{deadman.name} - {deadman.deaths} times! ☠️'
    await ctx.send(out)
    db_session.close()


# /events
@bot.command()
async def events(ctx: interactions.CommandContext):
    """Show any global events"""
    ephemeral = True
    logging.info(
        '%s (%i) / %s / events',
        ctx.channel, ctx.channel_id, ctx.user
    )

    # Find all global events
    global_events = models.GlobalEvent.query.all()

    # By default, assume there are none
    out = 'Unfortunately, there are no active events right now.'

    # Show any global events, and when they end
    if global_events:
        ephemeral = False
        out = f'Global Events ({len(global_events)}):\n'
        for event in global_events:
            out += f'{event.display_string} (ends in {event.end})\n'

    # Send the global events response
    await ctx.send(
        out,
        ephemeral=ephemeral
    )
    db_session.close()


# /mudhelp <search>
@bot.command(
    name='mudhelp',
    description='Find Ishar MUD help topic',
    options=[
        interactions.Option(
            name='search',
            description='title of a help topic to search for',
            type=interactions.OptionType.STRING,
            required=True
        )
    ]
)
async def mudhelp(
    ctx: interactions.CommandContext,
    search: str
):
    """Search for MUD help topics"""
    ephemeral = True
    logging.info(
        '%s (%i) / %s / mudhelp: "%s"',
        ctx.channel, ctx.channel_id, ctx.user, search
    )

    # Make sure that the search term is only letters
    if not regex.match(search):
        out = 'Sorry, but please limit your search to letters!'
        search_topics = {}

    # Try to find any help topics containing the search term
    else:
        out = 'Sorry, but no such help topics could be found!'
        search_topics = search_help_topics(
            all_topics=None,
            search=search
        )

    # By default, tell user if there were no results
    if search_topics:

        # Handle single search result, if there is only one
        num_results = len(search_topics)
        if num_results == 1:

            # Send the details of the single help topic to the channel
            ephemeral = False
            found_topic = next(iter(search_topics.values()))
            out = get_single_help(topic=found_topic)

        # Link search results to user, if there are multiple results
        elif num_results > 1:
            url = f'<https://isharmud.com/help/{search}>'.replace(' ', '%20')
            out = f'Search Results: {url} ({num_results} topics)'

    # Send the help search response
    await ctx.send(
        out,
        ephemeral=ephemeral
    )
    db_session.close()


# /spell <search>
@bot.command(
    name='spell',
    description='Find Ishar MUD spell help',
    options=[
        interactions.Option(
            name='search',
            description='name of a spell to search for',
            type=interactions.OptionType.STRING,
            required=True
        )
    ]
)
async def spell(
    ctx: interactions.CommandContext,
    search: str
):
    """Search for spells in MUD help topics"""
    ephemeral = True
    logging.info(
        '%s (%i) / %s / spell: "%s"',
        ctx.channel, ctx.channel_id, ctx.user, search
    )

    # Make sure that the search term is only letters
    if not regex.match(search):
        out = 'Sorry, but please limit your search to letters!'
        search_results = {}

    # Try to find any help topics containing the search term
    else:
        search_results = search_help_topics(
            all_topics=None,
            search=search
        )

    # Narrow down the results to any topic named starting with "Spell "
    search_spell_results = {}
    for name, topic in search_results.items():
        if name.startswith('Spell '):
            search_spell_results[name] = topic

    # By default, tell user if there were no results
    out = 'Sorry, but no such spell(s) could be found!'

    if search_spell_results:

        # Handle single search result, if there is only one
        num_results = len(search_spell_results)
        if num_results == 1:
            ephemeral = False
            found_spell = next(iter(search_spell_results.values()))
            out = get_single_help(topic=found_spell)

        # Show user the matching spell names, if there were 10 or less
        elif num_results <= 10:
            out = f'Found {num_results} spells: '
            out += ", ".join(search_spell_results.keys())

        # Otherwise, tell them to be more specific
        else:
            out = f'Sorry, but there were {num_results} results! '
            out += 'Please try to be more specific.'

    # Send the spell search response
    await ctx.send(
        out,
        ephemeral=ephemeral
    )
    db_session.close()


# /mudtime
@bot.command()
async def mudtime(ctx: interactions.CommandContext):
    """Show the MUD server time"""
    logging.info(
        '%s (%i) / %s / mudtime',
        ctx.channel, ctx.channel_id, ctx.user)

    # Find/show the server time
    now = datetime.utcnow().strftime('%A, %B %d, %Y @ %H:%M:%S (%I:%M:%S %p)')
    await ctx.send(f'The current Ishar MUD server time is: {now}')
    db_session.close()


# /connections
@bot.command()
async def connections(ctx: interactions.CommandContext):
    """Show the MUD process connections"""
    ephemeral = True
    logging.info(
        '%s (%i) / %s / connections',
        ctx.channel, ctx.channel_id, ctx.user
    )

    # Find/show the MUD process connections
    out = 'Sorry, but no connection information could be found.'
    conns = get_connections()
    if conns:
        ephemeral = False
        out = f'There are {len(conns)} unique connections to the MUD'
    await ctx.send(
        out,
        ephemeral=ephemeral
    )
    db_session.close()


# /uptime
@bot.command()
async def uptime(ctx: interactions.CommandContext):
    """Show the MUD process uptime"""
    ephemeral = True
    logging.info(
        '%s (%i) / %s / uptime',
        ctx.channel, ctx.channel_id, ctx.user
    )

    # Find/show the MUD process uptime
    out = 'Sorry, but no system information could be found.'
    utime = get_uptime()
    if utime:
        ephemeral = False
        out = f'Uptime: {utime}'
    await ctx.send(
        out,
        ephemeral=ephemeral
    )
    db_session.close()


# /season
@bot.command()
async def season(ctx: interactions.CommandContext):
    """Show the current Ishar MUD season"""
    logging.info(
        '%s (%i) / %s / season',
        ctx.channel, ctx.channel_id, ctx.user
    )

    # Get the current active season
    current = models.Season.query.filter_by(
        is_active=1
    ).order_by(-models.Season.season_id).first()

    # Show the current active season ID, and end date
    out = f'It is currently Season {current.season_id}'
    out += f', which ends in {current.expires}!'
    await ctx.send(out)
    db_session.close()


# /faq
@bot.command()
async def faq(ctx: interactions.CommandContext):
    """Link to the Frequently Asked Questions page"""
    logging.info(
        '%s (%i) / %s / faq',
        ctx.channel, ctx.channel_id, ctx.user
    )
    await ctx.send('https://isharmud.com/faq')
    db_session.close()


# /faqs
@bot.command()
async def faqs(ctx: interactions.CommandContext):
    """Link to the Frequently Asked Questions page"""
    logging.info(
        '%s (%i) / %s / faqs',
        ctx.channel, ctx.channel_id, ctx.user
    )
    await ctx.send('https://isharmud.com/faq')
    db_session.close()


# /get_started
@bot.command()
async def get_started(ctx: interactions.CommandContext):
    """Link to the Getting Started page"""
    logging.info(
        '%s (%i) / %s / get_started',
        ctx.channel, ctx.channel_id, ctx.user
    )
    await ctx.send('https://isharmud.com/get_started')
    db_session.close()


# /getstarted
@bot.command()
async def getstarted(ctx: interactions.CommandContext):
    """Link to the Getting Started page"""
    logging.info(
        '%s (%i) / %s / getstarted',
        ctx.channel, ctx.channel_id, ctx.user
    )
    await ctx.send('https://isharmud.com/get_started')
    db_session.close()


# Handle SIGTERM
def sigterm_handler(num, frame):
    """Try to exit gracefully on SIGTERM"""
    logging.info(
        'Caught SIGTERM: %i / %s',
        num, frame
    )
    db_session.close()
    sys.exit(0)


# Main execution of the bot
try:
    logging.info('Starting...')

    # Catch SIGTERM to shut down gracefully
    signal.signal(
        signal.SIGTERM,
        sigterm_handler
    )

    # Start the bot
    bot.start()

# Catch/log exceptions/errors,
#   send any errors to Sentry,
#   and exit with an error code (1)
except Exception as err:
    logging.exception(err)
    sentry_sdk.capture_exception(err)
    sys.exit(1)

# Say goodbye
finally:
    db_session.close()
    logging.info('Exiting...')
