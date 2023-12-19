# Trying CTF's from around the world

1. hacktify CTF


## excel worksheet

```
Sub CopyRowData()
    Dim inputSheet As Worksheet
    Dim outputSheet As Worksheet
    Dim inputRange As Range
    Dim outputRow As Long
    Dim lastRow As Long

    ' Define sheets - change "Sheet1" to your actual sheet name
    Set inputSheet = ThisWorkbook.Sheets("Sheet1")
    Set outputSheet = ThisWorkbook.Sheets("Sheet1") ' Change if the output is on a different sheet

    ' Define input range - change range as per your requirement
    Set inputRange = inputSheet.Range("D4:D13") ' Example range

    ' Find the last used row in the output area. Assuming output starts at column "I"
    lastRow = outputSheet.Cells(outputSheet.Rows.Count, "I").End(xlUp).Row

    ' Determine the row to paste the data
    If lastRow = 1 And IsEmpty(outputSheet.Cells(lastRow, "I").Value) Then
        outputRow = lastRow
    Else
        outputRow = lastRow + 1
    End If

    ' Copy-paste the data. Adjust the column ("I") if necessary
    inputRange.Copy
    outputSheet.Cells(outputRow, "I").PasteSpecial Paste:=xlPasteValues, Transpose:=True

    ' Optional: to remove any "marching ants" border that appears after copying
    Application.CutCopyMode = False
End Sub

```

easier formula

```
=CHOOSE(VALUE(MID(DAY, 4, LEN(DAY) - 3)), ELE!AE14, ELE!AE163, ELE!AE312, ELE!AE412, ELE!AE512, ELE!AE612, ELE!AE712, ELE!AE812, ELE!AE912, ELE!AE1012, ELE!AE1112, ELE!AE1212, ELE!AE1312, ELE!AE1412, ELE!AE1512, ELE!AE1612, ELE!AE1712, ELE!AE1812, ELE!AE1912, ELE!AE2012)
```