def extremelySimplePlagiarismChecker(text1,text2):
    l = len(text1)
    t = 0
    for i,c in enumerate(text1):
        if c == text2[i]:
            t+=1

    return (t/l)*100
