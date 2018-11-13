#Można usprawnić przeszukując binarnie lines jest posortowane, ale trzeba wtedy zmienić cały mechanizm
def GetTone(lines, distanceBetweenLines, yNotePosition):
    for i in range(len(lines)):
       #Jeżeli nuta jest w zasięgu tej pięciolinii
       if((yNotePosition > lines[i][0] - 2 * distanceBetweenLines) or (yNotePosition < lines[i][0] + 2.5 * distanceBetweenLines)):
            margin = distanceBetweenLines/4

            if(yNotePosition < lines[i][0] - 2*distanceBetweenLines + margin):
               return 'c3'

            elif(yNotePosition < lines[i][0] - distanceBetweenLines - margin):
                return 'h2'
            elif(yNotePosition < lines[i][0] -distanceBetweenLines + margin):
                return 'a2'

            elif(yNotePosition < lines[i][0] - margin):
                return 'g2'
            elif(yNotePosition < lines[i][0] + margin):
                return 'f2'

            elif(yNotePosition < lines[i][1] - margin):
                return 'e2'
            elif(yNotePosition < lines[i][1] +margin):
                return 'd2'

            elif(yNotePosition < lines[i][2] - margin):
                return 'c2'
            elif(yNotePosition < lines[i][2] + margin):
                return 'h1'

            elif(yNotePosition < lines[i][3] - margin):
                return 'a1'
            elif(yNotePosition < lines[i][3] + margin):
                return 'g1'

            elif(yNotePosition < lines[i][4] - margin):
                return 'f1'
            elif(yNotePosition < lines[i][4] + margin):
                return 'e1'

            elif(yNotePosition < lines[i][4] + distanceBetweenLines - margin):
                return 'd1'
            elif(yNotePosition < lines[i][4] + distanceBetweenLines + margin):
                return 'c1'

            elif(yNotePosition < lines[i][4] + 2*distanceBetweenLines - margin):
                return 'h'
            elif(yNotePosition < lines[i][4] + 2*distanceBetweenLines + margin):
                return 'a'

    return ''
