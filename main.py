import asyncio
import json
import logging
import pprint

import aiohttp
import src.app_logger as app_logger
from understat import Understat

log = app_logger.get_logger('main', level = logging.DEBUG)
pp = pprint.PrettyPrinter(indent = 4)

leagueName = 'RFPL'
async def main():
    async with aiohttp.ClientSession() as session:
        understat = Understat(session)
        league = await understat.get_league_table(
            league_name = leagueName, 
            season = 2022,
            # start_date='2023.08.01',
            # end_date = "2023.08.22",
        )
        log.info(f'\nLEAGUE "{leagueName}"')
        for row in league:
            print("{:<30} {:<6} {:<6} {:<6} {:<6} {:<6} {:<6} {:<6} {:<10} {:<10} {:<10} {:<10} {:<10} {:<10} {:<10} {:<10} {:<10} {:<10}".format(*row))
        # pp.pprint(league)
        # log.debug(league)
        # log.debug(json.dumps(league))

        leaguePlayers = await understat.get_league_players(
            league_name = leagueName, 
            season = 2022,
            # start_date='2023.08.01',
            # end_date = "2023.08.22",
        )
        log.info(f'\nLEAGUE "{leagueName}" PLAYERS')
        header = list(leaguePlayers[0].keys())
        #         1     2      3    4      5    6     7     8     9       10    11     12      13    14     15     16      17    18
        fmt = '{:<6} {:<30} {:<6} {:<6} {:<6} {:<7} {:<8} {:<6} {:<6} {:<12} {:<12} {:<12} {:<12} {:<30} {:<10} {:<10} {:<10} {:<10}'
        print(fmt.format(*header))
        for row in leaguePlayers:
            row['npxG'] = "{:.2f}".format(float(row['npxG']))
            row['xA'] = "{:.2f}".format(float(row['xA']))
            row['xG'] = "{:.2f}".format(float(row['xG']))
            row['xGBuildup'] = "{:.2f}".format(float(row['xGBuildup']))
            row['xGChain'] = "{:.2f}".format(float(row['xGChain']))
        for row in leaguePlayers:
            values = list(row.values())
            print(fmt.format(*values))
        # pp.pprint(leaguePlayers[0])
        # log.debug(leaguePlayers)
        # log.debug(json.dumps(leaguePlayers))

        await session.close()
if __name__ == '__main__':
    log.info('START')
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
