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

    ' Define sheets - change "Sheet1" to your sheet name
    Set inputSheet = ThisWorkbook.Sheets("Sheet1")
    Set outputSheet = ThisWorkbook.Sheets("Sheet1") ' Change if output is on a different sheet

    ' Define input range - change range as per your requirement
    Set inputRange = inputSheet.Range("A1:B1") ' Example range

    ' Find the last used row in the output area
    lastRow = outputSheet.Cells(outputSheet.Rows.Count, "D").End(xlUp).Row ' Change "D" to your start column in output area

    ' If it's the first time, start from the specific row; else, go to next row
    If lastRow = 1 And IsEmpty(outputSheet.Cells(lastRow, "D").Value) Then ' Change "D" to match above
        outputRow = lastRow
    Else
        outputRow = lastRow + 1
    End If

    ' Copy-paste the data
    inputRange.Copy Destination:=outputSheet.Cells(outputRow, "D") ' Change "D" to the start column of the output

End Sub

```