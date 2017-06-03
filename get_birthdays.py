import datetime
from calendar import monthrange
import requests
import random
import pyparsing as pp
import time
import wikipedia
import yaml

# prepare a list of slugs
slugs = []

months = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']

now = datetime.datetime.now()
year = now.year

for i in range(len(months)):
  num_days = monthrange(year, i+1)[1]
  for j in range(1, num_days+1):
    slug = '{0}-{1}'.format(months[i], j)
    slugs.append(slug)

births = {}

# visit all slugs
for slug in slugs:
  print slug
  query = slug.replace('-', ' ')

  # get the page
  page = wikipedia.page(query.title(), auto_suggest=False)

  # parse out the relevant chunk
  start = pp.Literal('== Births ==')
  end = pp.Literal('== Deaths ==')
  pattern = start.suppress() + pp.SkipTo(end)
  births_content = pattern.searchString(page.content)

  # prepare a list of [birth year, name / team] elements
  all_births = births_content[0][0].split('\n')
  all_births = [item.split(u'\u2013') for item in all_births if item]

  nba_teams = ['Atlanta Hawks', 'Boston Celtics', 'Brooklyn Nets', 'Charlotte Bobcats', 'Chicago Bulls', 'Cleveland Cavaliers', 'Dallas Mavericks', 'Denver Nuggets', 'Detroit Pistons', 'Golden State Warriors', 'Houston Rockets', 'Indiana Pacers', 'LA Clippers', 'LA Lakers', 'Memphis Grizzlies', 'Miami Heat', 'Milwaukee Bucks', 'Minnesota Timberwolves', 'New Orleans Hornets', 'New York Knicks', 'Oklahoma City Thunder', 'Orlando Magic', 'Philadelphia Sixers', 'Phoenix Suns', 'Portland Trail Blazers', 'Sacramento Kings', 'San Antonio Spurs', 'Toronto Raptors', 'Utah Jazz', 'Washington Wizards']
  wnba_teams = ['Atlanta Dream', 'Chicago Sky', 'Connecticut Sun', 'Indiana Fever', 'New York Liberty', 'Washington Mystics', 'Dallas Wings', 'Los Angeles Sparks', 'Minnesota Lynx', 'Phoenix Mercury', 'San Antonio Stars', 'Seattle Storm']

  basketball_player_births = []
  for item in all_births:
    birth_year = item[0]
    name_description = ' '.join(item[1:])

    if 'basketball player' in name_description:
      name = name_description.split(',')[0]

      try:
        summary = wikipedia.summary(name)
      except wikipedia.exceptions.DisambiguationError:
        continue

      team = ''
      for nba_team in nba_teams:
        if nba_team.lower() in summary.lower():
          team = nba_team
      for wnba_team in wnba_teams:
        if wnba_team.lower() in summary.lower():
          team = wnba_team

      if team:
        name_team = u"{0} of the {1}".format(name, team)

        temp = [birth_year.strip(), name_team.strip()]
        basketball_player_births.append(temp)

  # prepare template
  on_this_day = ''
  num_births = len(basketball_player_births)
  if num_births > 0:
    for item in basketball_player_births:
      birth_year, name_team = item
      on_this_day += u'{0} was born today in {1}.'.format(name_team, birth_year)
  else:
    on_this_day = 'No basketball players were born today.'

  # add to dict
  births[slug] = on_this_day

  # sleep
  interval = random.randrange(3, 5)
  print 'Sleeping for {0}s'.format(interval)
  print
  time.sleep(interval)

f = open('templates.yaml', 'w')
yaml.dump(births, f, default_flow_style=False, width=1000)
f.close()