
from pdb import pm


level = 0

DisplayConfiguration = {
    '1s': '╰╼╾╼',
    '1r': '    ╭',
    '2s': '    ╰╼╾╼',
    '2r': '       ╭',
    '3r': '       ╰╼╾╼'
}




def DisplayProgramMap(programMap: str, sender: str):

    pmListFull = programMap.split('\n')
    pmList = pmListFull[2:]
    print(f'{pmListFull[0]}\n{pmListFull[1]}')
    for line in pmList:
        if line == pmList[0]:
            line = '╰═╦═GetScoreboard.GetTodaysScoreboard╼╮'
        elif line in [pmList[1], pmList[2]]:
            if line[0] in ['╭', '╰'] :
                line = f'  ╠{line[4:]}'
            else:
                line = f'  ║{line[4:]}'



        elif line != pmList[0]:
            if line[0] in ['╭', '╰'] :
                line = f'  ╠{line[3:]}'
            else:
                line = f'  ║{line[3:]}'

        print(line)
    
    print('  ║\nDriver.Wait')



def DisplayFullProgramMap(fullProgramMap: list):
    for programMap in fullProgramMap:
        for line in programMap.split('\n'):
            print(line)
        test = 1
    test = 1


def DisplayOneProgramMap(programMap: str):
    for line in programMap.split('\n'):
        print(line)
    test = 1



def FormatProgramMap(programMap: str):
    pmListFull = programMap.split('\n')
    pmList = pmListFull[2:]
    #new
    newMap = f'◈ {pmListFull[1]}'
    for line in pmList:
        if line == pmList[0]:
            line = '        ╰═╦═GetScoreboard.GetTodaysScoreboard╼╮'
        elif line in [pmList[1], pmList[2]]:
            if line[0] in ['╭', '╰'] :
                line = f'          ╠{line[4:]}'
            else:
                line = f'          ║{line[4:]}'
        elif line != pmList[0]:
            if line[0] in ['╭', '╰'] :
                line = f'          ╠{line[3:]}'
            else:
                line = f'          ║{line[3:]}'
        newMap += f'\n{line}'
    newMap += '\n╔═════════╝'
    newMap += '\n╚╾Driver.Wait '
    newMap += '\n╔═══════╝'
    return newMap
    