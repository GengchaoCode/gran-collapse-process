opposites = {'up': 'down', 'right': 'wrong', 'true': 'false'}
alias = opposites.copy()

print(alias is opposites)

alias['right'] = 'left'
print(opposites['right'])