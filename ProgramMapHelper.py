
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
            line = '╰═╦═GetScoreboard.GetTodaysScoreboard╼╮ '
            t = line[0]
            t1 = line[1]
            t2 = line[2]
            t3 = line[3]
            a = 1


        elif line != pmList[0]:
            if line[0] in ['╭', '╰'] :
                line = f'  ╠{line[3:]}'
                t = line[0]
                t1 = line[1]
                t2 = line[2]
                t3 = line[3]
                a = 1
            else:
                line = f'  ║{line[3:]}'

        print(line)
    
    if sender == 'Wait':
        print('  ║\nWait')