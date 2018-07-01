import xlsxwriter, openpyxl

wb = xlsxwriter.Workbook("excel7.xlsx")
sheet = wb.add_worksheet("python")

def zeroFill():
    book = openpyxl.load_workbook("excel7.xlsx")
    ws = book.worksheets[0]
    with open('data4.txt') as f:
        f_line = f.readline().split()
        rowCount = f_line[0]
        colCount = f_line[1]
        for k in range(int(rowCount)):
            for i in range(int(colCount)):
                if ws.cell(int(k)+1,int(i)+1).value == None:
                    ws.cell(int(k)+1,int(i)+1).value=0
                   
    book.save("excel7.xlsx")

        
def main():
    r = -1
    with open('data4.txt') as f:
        line = f.readlines()
        for i in line:
            l = i.split()
            if len(l) == 1:
                r += 1
                continue
            else:
                for c in list(range(716)):
                    for j in l:
                        if c not in l:                        
                            sheet.write(int(r),int(j)-1,1)
    wb.close()
    zeroFill()


if __name__ == "__main__":
    main()
