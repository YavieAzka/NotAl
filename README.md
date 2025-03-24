# NotAl
NotAl (*Notasi Algoritma*) is a procedural programming language built using **Python**, designed to assist undergraduate students at **Institut Teknologi Bandung (ITB)** in learning **Algorithm and Programming 1**. 

This language entirely follows the structure and conventions outlined in the **"Diktat Pemrograman Prosedural"** by **Inggriani Liem (2007)**.

## Features
- Basic I/O: `input()`, `output()`
- assignment: `<-`
- Arithmetic operations
- Control flow: `if`, `else`, `for` (coming soon), `while` (coming soon) 
- Data types: integer, float, string, boolean `+`, `-`, `*`, `/`, `%`
## Installation
1. Make sure that you already have python installed in your device.
2. After downloading the 'notal.py' file, make sure that the file is located in the same folder as your .notal file.
3. run your .notal file by simply write:
   'python notal.py yourfilename.notal'

## Example
hello.notal
```notal
PROGRAM hello

KAMUS

ALGORITMA
output("Konichiwa Sekai!")
```
calc.notal
```notal
PROGRAM calc
{ Simple adder program }

KAMUS
a, b, c: integer

ALGORITMA
input(a)
input(b)
c <- a + b {c = a + b}
```
bestgirl.notal
```notal
PROGRAM bestgirl
{ Program for checking if your waifu is the best girl, or you just a karbit }

KAMUS
waifu, bestgirl: string

ALGORITMA
bestgirl <- "furina"
output("Who is the best girl?")
input(waifu)
if (waifu = bestgirl) then
    output("You're absolutely correct")
else
    output("Karbit")
```

## About Developer
NotAl is developed and maintained by **Yavie Azka de Fontaine**, a Computer Science undergraduate at **Institut Teknologi Bandung (ITB)**. This project was created to assist students taking **Algorithm and Programming 1** in running their **Notasi Algoritma** programs, ensuring they follow the correct **syntax** and **logic**. NotAl is still under active development, and I’m always open to **suggestions** and **questions**. Feel free to reach out to me on **Twitter**: [@yveakzontwt](https://twitter.com/yveakzontwt).

