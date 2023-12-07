# Trying CTF's from around the world

1. hacktify CTF


## excel worksheet

```
Dim counter As Integer

Sub CopyValueToAnotherSheet()
    ' Initialize counter if not already done
    If counter = 0 Then
        counter = 1
    Else
        counter = counter + 1
    End If

    ' Define the source and target worksheets and cells
    Dim sourceSheet As Worksheet
    Dim targetSheet As Worksheet
    Dim sourceCell As Range
    Dim targetCell As Range

    Set sourceSheet = ThisWorkbook.Worksheets("Sheet1") ' Change "Sheet1" to your source sheet name
    Set targetSheet = ThisWorkbook.Worksheets("Sheet2") ' Change "Sheet2" to your target sheet name
    Set sourceCell = sourceSheet.Range("A1") ' Change "A1" to your source cell
    Set targetCell = targetSheet.Cells(counter, 1) ' This will paste the value in column A, next available row

    ' Copy the value
    targetCell.Value = sourceCell.Value
End Sub
```