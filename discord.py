"""
Discord bot simply runs in a screen session, for now
So far, there are only two "slash commands" (/):
/season and /challenges
"""
from datetime import datetime
from dateutil.relativedelta import relativedelta
import interactions
import discord_secret
from database import db_session
from models import Challenge, Season

bot = interactions.Client(token=discord_secret.TOKEN, default_scope=discord_secret.GUILD)

@bot.command()
async def season(ctx: interactions.CommandContext):
    """Show the current Ishar MUD season information"""
    current_season  = Season.query.filter_by(is_active = 1).first()
    start_time = datetime.utcnow()
    end_time = current_season.expiration_date
    diff = relativedelta(start_time, end_time)
    diff_str = ""
    if diff.months > 0:
        diff_str += f"{diff.months} months, "
    diff_str += f"{diff.days} days , and {diff.hours} hours"
    await ctx.send(
        f'It is currently Season {current_season.season_id}, ' \
        f'which ends in {current_season.expires}, on ' \
        f"{diff_str}!"
    )
    db_session.close()

@bot.command()
async def challenges(ctx: interactions.CommandContext):
    """Show the current in-game Ishar MUD challenges"""
    current_challenges  = Challenge.query.filter_by(is_active = 1).order_by(
                            Challenge.adj_level,
                            Challenge.adj_people
                        ).all()
    count       = len(current_challenges)
    completed   = 0
    for challenge in current_challenges:
        if challenge.winner_desc != '':
            completed   = completed + 1
    await ctx.send(f"Challenges: {completed} completed / {count} total")
    db_session.close()

bot.start()
