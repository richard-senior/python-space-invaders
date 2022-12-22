###
## R.M.Senior 2022 - Simple Python Space Invaders
##
## To human beings:
##  You should be able to easily follow and modify this
##
## To ass-hats:
##      * Stealing something and saying you wrote it is straight up lame
##      * You can do it : better, smaller, faster, more efficiently, whilst playing the flute etc. Please go ahead.
##      * This is not pythonic... Yawn. Go learn Java
##      * This has been done a million times before (I know, but I've wanted to do this myself since I was 11)
##      * It's not completely accurate.. where is the space invader carrying the letter Y etc. (yes I know, I got as near as I could be bothered to)

import pygame
import base64
import io
import zipfile
import random
import copy

# ideas for a background image?
# https://dev.to/taarimalta/starry-night-with-python-turtle-1lo
# Improvement Ideas:
#    * animated player base ship

pygame.init()
pygame.mixer.init()

columns = 16
rows = 14
tick = 1
running = True
dead = 0
dying = 1
alive = 2
right = 1
playerSpeed = 4
alienSpeed = 600
speedupRate = 10
currentDirection = right
startRow = 1
invasionLevel = 1
currentStep = 0
left = -1
round = 1
scale = 4
width = 256 * scale
height = 224 * scale
rowSize = height / rows
colSize = width / columns
stepSize = 2 * scale
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
FPS = 60
o = []
################################## AUDIO ######################################
# Audio
# Base64'd zipfiles named VARNAME.zip, containing a wav named 's.wav'
# decode, unzip, extract wav, load wav into mixer
m1 = "UEsDBBQAAAAIABJ4i1VdZd6D/QEAAAIEAAAFAAAAcy53YXaVkiGsm0AcxllqVsWWoDDMoM6gUJgTe2QCc2JDXfLCsgSxYE6dwqAwKFRNFQpTVVVTVYUhE1U1VZgqxELSfXd7vD5R8fp99ydNevD/3Xd/9u3p6e/CMH7Q719//RZfPhmG8QH+TAyU+v3R+Pksnv9gj0zjgFjm0nI8ytO8arb742m4jNN1mqZxvAynY3fYbzfNuioLKdIkZiH1A0ojxnnMWRh4rr0w7mlh2o4XhBHPZF7WzWZ36NSnr+/QOAznU98f9rrzqq7LIpciSxPOGYsiSsH8tpVpkyBiSSpErqX3pjxmEQ084jo2TrhYKKal7XoQcW1zeZ/ZBXOcCo28747DeH1c0wXB9R3wW+CDvshzIIEoJOatG2D8kPE0E0JKmUspRJYloEbEhDiWeQsW5KZlWjfmu+zED+Mkk0W9bneH/vQgu77tvjvstpu2WQF7ThI3TYl564NZAbXIi7Kq66quyrLA8RJ1N4Gvs0XcrzNAiOvqs9yHdohHI57KvFo1WwR+vkwPRT0OZ1DrId20q3qmTnisggypItIz4NiQZYHtxaYuy1bG35DrEkI83/MDPwhoSMMojBiLMehJgoFKM3VT+X8VOH6JVSGBlfJaGWrWTdu0raqN9rzmR9O0sN6otuu38D5Uq6qqWruEsVQPVFGoQtdZQsLgAZP2m0f2D1BLAQI/ABQAAAAIABJ4i1VdZd6D/QEAAAIEAAAFACQAAAAAAAAAIAAAAAAAAABzLndhdgoAIAAAAAAAAQAYAAYiNlJxDdkBoT8LtXMN2QEAV0EB04y+AVBLBQYAAAAAAQABAFcAAAAgAgAAAAA="
m2 = "UEsDBBQAAAAIABl4i1X06gKLKAIAAD4EAAAFAAAAcy53YXaVUyGMo0AU5cKJQ3F3QWHmDAqDQmEQt5MTGMQdimTD5RLEBTMKNQaFQaEwKBQGhVpTVVVTVVVTVVNV1aT3/rRpttlLNv1vmDKT/pn/3vvEP56e/I+a9iv8+f3PX/Hts6ZpH4AvroaH3j9pv5/F81f8R0qRcp9ZhsW8MMll3U8vq83ucDqdzmdMh8Nuu14t53ns20bKssjSOAoD3+c8TtJULRxmav8J3bBs1w95komyarphmhc4eX/Ewe/E6XjYbzeb1XLxMk/j0HdN3VS4XIg8T9MkjqIwDFCD57qOw5htm/rdzZbj8zjNi1JWVV3VNR4JoqIosgQVcyR7rsMc1+cRSCRJxAPfZdbrY3TdtJjrBTzOcE7dDtPLcr3dH88PxulGZZqGrm3qSvHIIB2PuCLhgIFNl9+FybwA1WW5EGUpSyQVyEqU+p7nMGQYuqZrho0yseMyJcPbAA/YAD1KCRfmi72Pcthtr3ZMsINIVBJy5imku1gBL6gm/e5m28O9kI98qBsAieQD8Yg5eKgcAEKHYchD7KAX39CgTiI1ciGrph/hxGMcrh21Xi7mGQTIBnkpRFUSqY5WDFQ5pmmZCANh0tANLABsW3CKMYbmcVyS3fcDVM55FMVxArfgV16IQnkG2hL9R8Sbtuu6tusJ/TCMNEaax4mghpponoHbBj0DXlXG0A89qm9BoFEDqipUEBiAzrj0itdREtBD6CI1F/QxCIXbLwYt/gFQSwECPwAUAAAACAAZeItV9OoCiygCAAA+BAAABQAkAAAAAAAAACAAAAAAAAAAcy53YXYKACAAAAAAAAEAGACLLjxbcQ3ZAWO8W/NzDdkBAFdBAdOMvgFQSwUGAAAAAAEAAQBXAAAASwIAAAAA"
m3 = "UEsDBBQAAAAIACR4i1VoEkKOIgIAAEoEAAAFAAAAcy53YXaVUiGMnEAUpaGiKNoEhSg1KAwKhaFJj1RgVrQokgtNE0SDGYUaMwqDQmFQKAwKhVm1qmbVqjWr1qxatcn1/RlObNJc7t6b+Sw7M//Pe5/N94eHr+817Wf049vvP+zLR03T3oGfPA2Tfn/Qfj2yx8/Yw7kQXHCWxYFjmZYTxGnJ237eHY6Xy+1J4na9nk+H/W47j33X1Lwqi2yTxFEQRskmy7I0jUPftQztf9AtxwvCJCtYJZqun5bt/nC6XJ9egevlfD7u/6LuPKJy2wjOq4oVRY6SSRJFYeh7jmPblo2rm6ZpGKYB6DqFu1uYbpBkJacbjOO8LPMyU9Jh6DqZFZKgI4njJM3LquIVI40ky4EtyIacumlZjusFkdzDVzHHE2x6C25kJlQtyzRIO6kYFMFRCAp8T0kySYKuvQjLlcaih3XTtl3bNk0tZL7iOaGPfHTlLMtzCIwCz7HNu7S6YdmuH6KTEFW3w7TsqEFv1HRRorbzJDtFprISnUo38hoB6XKlMLTKAMhSFAdVhL/onolVy3Zs+Ox6Pk4FYRhFaEuySdH0LC+KsmT4CDggSHeD0Ur1Xdf3AzAO4zhN0wjOxJmaTZG4qOekFuQuDHUIARnAru+AlojkVKIWQg0UvQO+FUnGKrBkrCzlKEoMEMhX0n/0qibewXUbTuCsCvQEVEYV1Rq9Eakex1yxOiEQyZBagM06a0T4s456jc+kQLhfVyfU2j9QSwECPwAUAAAACAAkeItVaBJCjiICAABKBAAABQAkAAAAAAAAACAAAAAAAAAAcy53YXYKACAAAAAAAAEAGAAaOvRlcQ3ZAWgpiw50DdkBAFdBAdOMvgFQSwUGAAAAAAEAAQBXAAAARQIAAAAA"
m4 = "UEsDBBQAAAAIAEB4i1Wab/YPGAIAAHYEAAAFAAAAcy53YXaVkyGM2zAUhjN1YEXdpEMhGQkKKQoyCdhZmxRisAVFOmWaZLCFGAWZBIUEBYUYGZkEFYUEBYUEFYUElRQVVbq91/bWgZPa+9+z7KrJy+f/2ezr4+Of95b1I/j+5ddv8fmjZVnvID55Fgxcf7B+Pomnb/BMnstcyjwvYEZJTFxmSeg7D8uV7ZEokYXa9Nt5f3i+6Hjc76bt0LcbXVe5zARPGKOUEEJZHMVJxALfc1YL6zUtVrbrk5AlaSaLSpu2H7fzDmvf1mE3T9PYdxuVp4x4ruN6fsBiLrK8KCullFZ1VZWFPDOFgOHawPFG4bbDOJVFbZpunPbH57fpuBuaSqZJws97bNoeNjlN8wT0I/pmVFXIjMcRItr26p85y+XiNu4CASlLBBRXzcnAw/EusAM2buxMAQ2mQUDROyxiNm3X9RBd2xiNcBINpGTt2g/L/z8NuuWeA3AxwtVm0w3Tnb29nq1pMKXkEYtYDP6V0IR2GMYtGHjyrtE18qVJFNKX/l7tWy0Xt5tLoxOehsLb+f72on8z+Dd0QGEAo4SLg2ct5UkcsTBETwnx157nung6HRsD5TgODNfFhL88z1t7a98nPiEBDSgNQxYyFsHl4QnnPE2FEFkmMonXE7KAA17CGa+quqpBqlZaa6WN0ZcANRCYRmNehlbXqBW8iiUAvYTEiucJ6uMocEP5KV6UAYgAHoj0OvPrGn+Jv1BLAQI/ABQAAAAIAEB4i1Wab/YPGAIAAHYEAAAFACQAAAAAAAAAIAAAAAAAAABzLndhdgoAIAAAAAAAAQAYAB76moRxDdkBIYzGHnQN2QEAV0EB04y+AVBLBQYAAAAAAQABAFcAAAA7AgAAAAA="
shot = "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"
hit = "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"
################################## SPRITES ####################################
# 8x8 pixel arrays encoded as bytes then encoded as integers 
# a-z
letters = [4547873299252292, 16963558462211132, 15837382733743160, 16963558596428860, 34907313345397884, 34907313345397764, 33781412505339000, 19215359349638212, 15780259870806072, 18085043209520184, 19179966936917060, 1130315200595068, 19259407863137348, 19215393040385092, 15837658689586232, 16963558458000388, 15837658690626648, 16963558459057220, 15837383610090552, 34920558287130640, 19215358410114104, 19215358410106896, 19215358679608388, 19215237276779588, 19215237275193360, 34973403564213372]
# 0, 1, 2, 3, 4, 5, 6, 7, 8, 9
numbers = [15837796397499448, 4530056895402040, 15837641170224252, 34973404104770616, 9060148223680544, 34907553934623800, 31534011675591736, 34973403564214280, 15837658488259640, 15837659561730076]
# SPACE, <, >, -
specialCharacters = [0, 9024825868161056, 2269530514526216, 2080374784]

# player shot
r0 = [0, 1, 0]
r1 = [0, 1, 0]
r2 = [0, 1, 0]
r3 = [0, 1, 0]
r4 = [0, 1, 0]
r5 = [0, 1, 0]
r6 = [0, 1, 0]
r7 = [0, 0, 0]
plshot1 = [r0, r1, r2, r3, r4, r5, r6, r7]
## squiggly shot
r0 = [0, 1, 0]
r1 = [1, 0, 0]
r2 = [0, 1, 0]
r3 = [0, 0, 1]
r4 = [0, 1, 0]
r5 = [1, 0, 0]
r6 = [0, 1, 0]
r7 = [0, 0, 0]
sshot1 = [r0, r1, r2, r3, r4, r5, r6, r7]
r0 = [1, 0, 0]
r1 = [0, 1, 0]
r2 = [0, 0, 1]
r3 = [0, 1, 0]
r4 = [1, 0, 0]
r5 = [0, 1, 0]
r6 = [0, 0, 1]
r7 = [0, 0, 0]
sshot2 = [r0, r1, r2, r3, r4, r5, r6, r7]
r0 = [0, 1, 0]
r1 = [0, 0, 1]
r2 = [0, 1, 0]
r3 = [1, 0, 0]
r4 = [0, 1, 0]
r5 = [0, 0, 1]
r6 = [0, 1, 0]
r7 = [0, 0, 0]
sshot3= [r0, r1, r2, r3, r4, r5, r6, r7]
r0 = [0, 0, 1]
r1 = [0, 1, 0]
r2 = [1, 0, 0]
r3 = [0, 1, 0]
r4 = [0, 0, 1]
r5 = [0, 1, 0]
r6 = [1, 0, 0]
r7 = [0, 0, 0]
sshot4= [r0, r1, r2, r3, r4, r5, r6, r7]
## rolling shot
r0 = [0, 1, 0]
r1 = [0, 1, 0]
r2 = [0, 1, 0]
r3 = [0, 1, 0]
r4 = [0, 1, 0]
r5 = [0, 1, 0]
r6 = [0, 1, 0]
r7 = [0, 0, 0]
rshot1 = [r0, r1, r2, r3, r4, r5, r6, r7]
r0 = [0, 1, 0]
r1 = [0, 1, 0]
r2 = [1, 1, 0]
r3 = [0, 1, 1]
r4 = [0, 1, 0]
r5 = [1, 1, 0]
r6 = [0, 1, 1]
r7 = [0, 0, 0]
rshot2 = [r0, r1, r2, r3, r4, r5, r6, r7]
r0 = [0, 1, 0]
r1 = [0, 1, 0]
r2 = [0, 1, 0]
r3 = [0, 1, 0]
r4 = [0, 1, 0]
r5 = [0, 1, 0]
r6 = [0, 1, 0]
r7 = [0, 0, 0]
rshot3= [r0, r1, r2, r3, r4, r5, r6, r7]
r0 = [0, 1, 1]
r1 = [1, 1, 0]
r2 = [0, 1, 0]
r3 = [0, 1, 1]
r4 = [1, 1, 1]
r5 = [0, 1, 0]
r6 = [0, 1, 0]
r7 = [0, 0, 0]
rshot4= [r0, r1, r2, r3, r4, r5, r6, r7]
## Plunger shot
r0 = [0, 1, 0]
r1 = [0, 1, 0]
r2 = [0, 1, 0]
r3 = [0, 1, 0]
r4 = [0, 1, 0]
r5 = [1, 1, 1]
r6 = [0, 0, 0]
r7 = [0, 0, 0]
pshot1 = [r0, r1, r2, r3, r4, r5, r6, r7]
r0 = [0, 1, 0]
r1 = [0, 1, 0]
r2 = [0, 1, 0]
r3 = [1, 1, 1]
r4 = [0, 1, 0]
r5 = [0, 1, 0]
r6 = [0, 0, 0]
r7 = [0, 0, 0]
pshot2 = [r0, r1, r2, r3, r4, r5, r6, r7]
r0 = [0, 1, 0]
r1 = [0, 1, 0]
r2 = [1, 1, 1]
r3 = [0, 1, 0]
r4 = [0, 1, 0]
r5 = [0, 1, 0]
r6 = [0, 1, 0]
r7 = [0, 0, 0]
pshot3= [r0, r1, r2, r3, r4, r5, r6, r7]
r0 = [1, 1, 1]
r1 = [0, 1, 0]
r2 = [0, 1, 0]
r3 = [0, 1, 0]
r4 = [0, 1, 0]
r5 = [0, 1, 0]
r6 = [0, 1, 0]
r7 = [0, 0, 0]
pshot4= [r0, r1, r2, r3, r4, r5, r6, r7]
r0 = [0, 0, 1, 0, 0, 0]
r1 = [1, 0, 0, 0, 1, 0]
r2 = [0, 0, 1, 1, 0, 1]
r3 = [0, 1, 1, 1, 1, 0]
r4 = [1, 0, 1, 1, 1, 0]
r5 = [0, 1, 1, 1, 1, 1]
r6 = [1, 0, 1, 1, 1, 0]
r7 = [0, 1, 0, 1, 0, 1]
ashotexp= [r0, r1, r2, r3, r4, r5, r6, r7]

r0 = [1, 0, 0, 0, 1, 0, 0, 1]
r1 = [0, 0, 1, 0, 0, 0, 1, 0]
r2 = [0, 1, 1, 1, 1, 1, 1, 0]
r3 = [1, 1, 1, 1, 1, 1, 1, 1]
r4 = [1, 1, 1, 1, 1, 1, 1, 1]
r5 = [0, 1, 1, 1, 1, 1, 1, 0]
r6 = [0, 0, 1, 0, 0, 1, 0, 0]
r7 = [1, 0, 0, 1, 0, 0, 0, 1]
rshotexp = [r0, r1, r2, r3, r4, r5, r6, r7]

r0 = [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]
r1 = [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0]
r2 = [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0]
r3 = [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0]
r4 = [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0]
r5 = [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0]
r6 = [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0]
r7 = [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0]
player1 = [r0, r1, r2, r3, r4, r5, r6, r7]
r0 = [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
r0 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0]
r2 = [0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0]
r3 = [0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
r4 = [0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0]
r5 = [0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0]
r6 = [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0]
r7 = [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1]
playerEx1 = [r0, r1, r2, r3, r4, r5, r6, r7]
r0 = [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0]
r0 = [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1]
r2 = [0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0]
r3 = [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
r4 = [0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1]
r5 = [0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0]
r6 = [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0]
r7 = [0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0]
playerEx2 = [r0, r1, r2, r3, r4, r5, r6, r7]
### TOP
r0 = [0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0]
r1 = [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0]
r2 = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0]
r3 = [0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0]
r4 = [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0]
r5 = [0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0]
r6 = [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0]
r7 = [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]
top1 = [r0, r1, r2, r3, r4, r5, r6, r7]
r0 = [0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0]
r1 = [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0]
r2 = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0]
r3 = [0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0]
r4 = [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0]
r5 = [0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0]
r6 = [0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0]
r7 = [0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0]
top2 = [r0, r1, r2, r3, r4, r5, r6, r7]
### MID
r0 = [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]
r1 = [0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0]
r2 = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0]
r3 = [0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0]
r4 = [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0]
r5 = [0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0]
r6 = [0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0]
r7 = [0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0]
mid1 = [r0, r1, r2, r3, r4, r5, r6, r7]
r0 = [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]
r1 = [0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0]
r2 = [0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0]
r3 = [0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0]
r4 = [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0]
r5 = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0]
r6 = [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]
r7 = [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0]
mid2 = [r0, r1, r2, r3, r4, r5, r6, r7]
## BOTTOM
r0 = [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0]
r1 = [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0]
r2 = [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0]
r3 = [0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0]
r4 = [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0]
r5 = [0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0]
r6 = [0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0]
r7 = [0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0]
bot1 = [r0, r1, r2, r3, r4, r5, r6, r7]
r0 = [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0]
r1 = [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0]
r2 = [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0]
r3 = [0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0]
r4 = [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0]
r5 = [0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0]
r6 = [0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0]
r7 = [0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0]
bot2 = [r0, r1, r2, r3, r4, r5, r6, r7]
### ALIEN EXPLOSION
r0 = [0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0]
r1 = [0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0]
r2 = [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0]
r3 = [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]
r4 = [0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0]
r5 = [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]
r6 = [0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0]
r7 = [0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0]
exp1 = [r0, r1, r2, r3, r4, r5, r6, r7]
r0 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
r1 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
r2 = [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0]
r3 = [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0]
r4 = [0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0]
r5 = [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0]
r6 = [0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0]
r7 = [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]
saucer1 = [r0, r1, r2, r3, r4, r5, r6, r7]
r0 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
r1 = [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0]
r2 = [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0]
r3 = [0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0]
r4 = [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0]
r5 = [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0]
r6 = [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0]
r7 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
saucerExp = [r0, r1, r2, r3, r4, r5, r6, r7]

r0 = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0]
r1 = [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0]
r2 = [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0]
r3 = [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0]
r4 = [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0]
r5 = [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0]
r6 = [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0]
r7 = [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0]
r8 = [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0]
r9 = [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0]
ra = [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0]
rb = [0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0]
rc = [0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0]
rd = [0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0]
re = [0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0]
rf = [0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0]
shield1 = [r0, r1, r2, r3, r4, r5, r6, r7, r8, r9, ra, rb, rc, rd, re, rf]

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)

TRANSPARENT = (0,0,0,0)

################### Objects
class Sample():
    def __init__(self, sample):
        d = base64.b64decode(sample)
        f = io.BytesIO(d)
        z = zipfile.ZipFile(f)
        # print(z.namelist())
        w = z.read("s.wav")
        wf = io.BytesIO(w)
        self.sound = pygame.mixer.Sound(wf)
        self.setVolume(0.1)
        
    def setVolume(self, vol):
        self.sound.set_volume(vol)
    def isPlaying(self):
        # TODO THIS!
        return False
    def play(self):
        if self.isPlaying(): return
        pygame.mixer.find_channel(True).play(self.sound)

# Things can be alive, dying, or dead
# This object keeps a record of that state
class StateAware():
    def __init__(self):
        self.state = alive
    def getState(self): return self.state
    def setState(self, state): self.state = state
    def isAlive(self): return self.getState() == alive
    def isDead(self): return self.getState() == dead
    def isDying(self): return self.getState() == dying
    def reset(self): pass

# Class that deals with animating and moving things around at different speeds
class TimedSprite(StateAware):
    def __init__(self):
        StateAware.__init__(self)
        self.lastAnimationTick = 0
        self.lastMoveTick = 0
        self.animationTickRate = 500
        self.moveTickRate = 500
    def getDrawColour(self): return (255, 255, 255)
    def setAnimationTickRate(self, tr): self.animationTickRate = tr
    def getAnimationTickRate(self): return self.animationTickRate
    def setMoveTickRate(self, tr): self.moveTickRate = tr
    def getMoveTickRate(self): return self.moveTickRate
    def onUpdate(self): pass
    def animate(self): pass
    def move(self): pass
    def update(self):
        self.onUpdate()
        tr = pygame.time.get_ticks()
        if tr - self.lastAnimationTick > self.getAnimationTickRate():
            self.lastAnimationTick = tr
            self.animate()
        if tr - self.lastMoveTick > self.getMoveTickRate():
            self.lastMoveTick = tr
            if self.isAlive(): self.move()

# class that displays numbers, letters and screen artifacts like the scrore etc.
class CharacterSurface(TimedSprite):
    lives = 3
    score = 0
    scoreDisplay = []
    headerDisplay = []
    footerDisplay = []
    l = []
    n = []
    sc = []
    # deals with 8x8 pixel characters encoding and decoding them to integers
    # assumes an 8x8 pixel array. ie [[0,0,0,1,0,1,0,0], [0,1,0,1,0,0,0,0]....]
    def __init__(self, encoded):
        TimedSprite.__init__(self)
        self.x = -50
        self.y = -50
        d = CharacterSurface.decode(encoded)
        f = PixelSprite.createFrames([d], self.getDrawColour())
        f, r, m = PixelSprite.scale(f, scale)
        self.frame = f[0]
    
    def getDrawColour(self): return GREEN

    def update(self):
        if not self.isAlive(): return
        screen.blit(self.frame, (self.x, self.y))
    
    @staticmethod
    def updateAll():
        for n in CharacterSurface.scoreDisplay: n.update()
        for n in CharacterSurface.headerDisplay: n.update()
        for n in CharacterSurface.footerDisplay: n.update()

        #for cs in CharacterSurface.l: cs.update()
        #for cs in CharacterSurface.n: cs.update()

    @staticmethod
    def addToScore(number): 
        CharacterSurface.score += number
        CharacterSurface.updateScore()

    @staticmethod
    def updateScore():
        sd = []
        for a in reversed(range(0, 4)):
            d = CharacterSurface.score // 10 ** a % 10
            s = copy.copy(CharacterSurface.n[d])
            s.y = s.frame.get_height() + (scale * 4)
            s.x = colSize * 4 - (s.frame.get_width() * a)
            s.setState(alive)
            sd.append(s)
        CharacterSurface.scoreDisplay = sd

    @staticmethod
    def encodeTest():
        r0 = [0, 0, 0, 0, 0, 0, 0, 0]
        r1 = [0, 0, 0, 0, 0, 0, 0, 0]
        r2 = [0, 0, 0, 0, 0, 0, 0, 0]
        r3 = [0, 0, 0, 0, 0, 0, 0, 0]
        r4 = [0, 0, 0, 0, 0, 0, 0, 0]
        r5 = [0, 0, 0, 0, 0, 0, 0, 0]
        r6 = [0, 0, 0, 0, 0, 0, 0, 0]
        r7 = [0, 0, 0, 0, 0, 0, 0, 0]

        r0 = [0, 0, 0, 0, 0, 0, 0, 0]
        r1 = [0, 0, 1, 1, 1, 0, 0, 0]
        r2 = [0, 1, 0, 0, 0, 1, 0, 0]
        r3 = [0, 1, 0, 0, 0, 1, 0, 0]
        r4 = [0, 0, 1, 1, 1, 0, 0, 0]
        r5 = [0, 1, 0, 0, 0, 1, 0, 0]
        r6 = [0, 1, 0, 0, 0, 1, 0, 0]
        r7 = [0, 0, 1, 1, 1, 0, 0, 0]

        a = [r0, r1, r2, r3, r4, r5, r6, r7]
        print(CharacterSurface.encode(a))

    @staticmethod
    def createString(s, x, y):
        ret = []
        i = 0
        for c in s:
            obj = None
            ln = ord(c)
            if ln >= 65 and ln <= 90: obj = CharacterSurface.l[ln - 65]
            elif ln >= 97 and ln <= 122: obj = CharacterSurface.l[ln - 97]
            elif ln >= 48 and ln <= 57: obj = CharacterSurface.n[ln - 48]
            elif ln == 32: obj = CharacterSurface.sc[0]
            # SPACE, <, >, -
            elif ln == 60:  obj = CharacterSurface.sc[1]
            elif ln == 62:  obj = CharacterSurface.sc[2]
            elif ln == 45:  obj = CharacterSurface.sc[3]
            else: raise ValueError("unknown character " + c + " which has code " + str(ord(c)))
            clone = copy.copy(obj)
            # TODO move x's based on width of letters and position in string
            clone.setState(alive)
            clone.x = x + (i * clone.frame.get_width())
            clone.y = y
            ret.append(clone)
            i += 1
        return ret

    @staticmethod
    def initCharacters():
        for l in letters: CharacterSurface.l.append(CharacterSurface(l))
        for n in numbers: CharacterSurface.n.append(CharacterSurface(n))
        for s in specialCharacters: CharacterSurface.sc.append(CharacterSurface(s))
        CharacterSurface.addToScore(0)
        CharacterSurface.headerDisplay = CharacterSurface.createString("score<1> hi-score score<2>", colSize * 2, 1)
        CharacterSurface.footerDisplay = CharacterSurface.createString("credit", width - colSize * 5, height - rowSize)
        #CharacterSurface.headerDisplay = CharacterSurface.createString("abcdefghijklmnopqrstuvwxyz 0123456789 <> -", 10, 40)
        # CharacterSurface.encodeTest()
    
    @staticmethod
    def decode(i):
        ba = bytearray(i.to_bytes(8, byteorder='big'))
        rows = []
        for b in ba:
            row = [0,0,0,0,0,0,0,0]
            integer = b
            n = -1
            while(integer > 0):
                digit = integer % 2
                row[n] = digit
                n += 1
                integer = integer // 2
            rows.append(row)
        return rows

    @staticmethod
    def encode(a):
        # assume 8x8 pixel array
        ret = []
        bytes_array = bytearray()
        for x in range(0, 8):
            sum = 0
            for y in reversed(range(0, 8)):
                if a[x][y]:
                    sum += 2 ** (y + 1)
            bytes_array.append(sum)
        # encode to int
        ret = int.from_bytes(bytes_array, "big")
        return ret

# class which deals with loading, scaling, animating and collision detecting and the pixelated (arrays of 1's and 0's) images above
class PixelSprite(TimedSprite):
    def __init__(self, pixelArrays, expArrays):
        TimedSprite.__init__(self)
        self.currentFrame = 0
        self.x = 0
        self.y = 0
        self.explosion_frames = []
        f = PixelSprite.createFrames(pixelArrays, self.getDrawColour())
        self.frames, self.rects, self.masks = PixelSprite.scale(f, scale)
        f = PixelSprite.createFrames(expArrays, self.getDrawColour())
        self.explosion_frames, self.explosion_rects, self.exposion_masks = PixelSprite.scale(f, scale)
        self.width = self.frames[0].get_width()
        self.height = self.frames[0].get_height()
        self.currentlyDisplayedFrame = self.frames[0]

    @staticmethod
    def createFrames(aa, colour):
        ret = []
        w = len(aa[0][0])
        h = len(aa[0])
        # create images (surfaces) from pixel arrays
        for a in aa:
            s = pygame.Surface((w, h), pygame.SRCALPHA | pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE)
            ca = pygame.PixelArray(s)
            for x in range(0, w):
                for y in range(0, h):
                    if a[y][x]:
                        ca[x, y] = colour
            del ca
            ret.append(s)
        return ret

    @staticmethod
    def scale(surfaces, scale):
        ret = []
        rs = []
        ms = []
        for f in surfaces:
            w = f.get_width() * scale
            h = f.get_height() * scale
            foo = pygame.transform.scale(f, (w, h))
            ret.append(foo)
            m = pygame.mask.from_surface(foo)
            ms.append(m)
            r = foo.get_bounding_rect()
            rs.append(r)
        return ret, rs, ms

    def getRect(self):
        # returns a rectangle that bounds the visible pixels of this current frame
        # for use in collision detection 
        r = self.rects[self.currentFrame]
        ret = pygame.Rect(self.x + r.x, self.y + r.y, r.width, r.height)
        return ret
    def getHeight(self): return self.getRect().height
    def getWidth(self): return self.getRect().width
    def getMask(self):
        return self.masks[self.currentFrame]

    def getCentreX(self):
        return self.getRect().centerx

    def isInline(self, obj):
        # is the passed object directly above or below us (is it's centre within our x width?) 
        ar = self.getRect()
        ac = self.getCentreX()
        br = obj.getRect()
        bc = obj.getCentreX()
        return ac > br.left and ac < br.right and bc > ar.left and bc < ar.right

    def checkMaskCollision(self, other):
        xoffset = other.getRect().x - self.getRect().x
        yoffset = other.getRect().y - self.getRect().y
        leftmask = self.getMask()
        rightmask = other.getMask()
        return leftmask.overlap(rightmask, (xoffset, yoffset))

    def checkCollision(self, other):
        if self.state != alive or other.state !=  alive: return
        if self is other: return
        o = other.getRect()
        t = self.getRect()
        if not o.colliderect(t): return
        # do more precise mask based collision detection for Shields
        if isinstance(self, Shield) and isinstance(other, Shot):
            if not self.checkMaskCollision(other): return
        self.onHitEvent(other)
        other.onHitEvent(self)

    def onHitEvent(self, other):
        self.currentFrame = 0
        self.state = dying

    def animate(self):
        self.currentFrame += 1
        if self.isAlive() and self.currentFrame >= len(self.frames):
            self.currentFrame = 0
        elif self.isDying() and self.currentFrame >= len(self.explosion_frames):
            self.state = dead

    def onUpdate(self):
        if self.isDead(): return
        if self.isAlive():
            self.currentlyDisplayedFrame = self.frames[self.currentFrame]
        elif self.isDying():
            self.currentlyDisplayedFrame = self.explosion_frames[self.currentFrame]
        screen.blit(self.currentlyDisplayedFrame, (self.x, self.y))
        #r = self.getRect()
        #pygame.draw.rect(screen,WHITE,r)

# there are 4 different kinds of shot in Space Invaders
# This class deals with shots, and causes all the collision detection to be run
class Shot(PixelSprite):
    # 0 = squiggly shot, 1 = ripply shot, 2 = ? shot, 3 = player short, 4 plungershot
    SA = [[plshot1], [sshot1, sshot2, sshot3, sshot4], [rshot1, rshot2, rshot3, rshot4], [rshot1, rshot2, rshot3, rshot4], [pshot1, pshot2, pshot3, pshot4]]
    sound = Sample(shot)

    def __init__(self, kind):
        self.x = -10
        self.y = -10
        self.kind = kind
        PixelSprite.__init__(self, Shot.SA[kind], [ashotexp])
        Shot.sound.setVolume(0.1)
        self.state = dead
        self.setAnimationTickRate(100)
        self.setMoveTickRate(1)
    
    def onHitEvent(self, other):
        if isinstance(other, Shot): 
            PixelSprite.onHitEvent(self, other)
        elif isinstance(other, Shield):
            # allow shot to penetrate shield before exploding
            # TODO player shots are reversed!
            if self.y > (other.y - (self.getHeight() / 3)):
                PixelSprite.onHitEvent(self, other)
        else:
            self.setState(dead)

    @staticmethod
    def getShotType(shotType):
        s = None
        for s in o: 
            if isinstance(s, Shot) and s.kind == shotType: return s
        s = Shot(shotType)
        o.append(s)
        return s

    @staticmethod
    def fire(obj, shotType):
        # is this shot-type available?
        s = Shot.getShotType(shotType)
        if not s.isDead(): return
        # should we fire?
        s.x = obj.getCentreX() - (s.width / 2)
        if isinstance(obj, Player):
            Shot.sound.play()
            s.y = obj.y - s.height
        else:
            # wait a second before allowing aliens to fire
            if pygame.time.get_ticks() < 1000: return
            # TODO random number
            s.y = obj.y + obj.height
        s.setState(alive)
        s.currentFrame = 0

    def move(self):
        if self.kind > 0:
            self.y += 6
        else:
            self.y += -12
        if self.y < 0 or self.y > height: self.state = dead
        for a in o: 
            if a is not self: a.checkCollision(self)


class Alien(PixelSprite):
    SA = [[top1, top2], [mid2, mid1], [mid1, mid2], [bot1, bot2], [bot2, bot1]]
    EA = [exp1]
    move_sounds = [Sample(m4), Sample(m1), Sample(m2), Sample(m3)]
    hit_sound = Sample(hit)

    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.currentSound = 0
        PixelSprite.__init__(self, Alien.SA[row], Alien.EA)
        self.move()

    def getAnimationTickRate(self): return alienSpeed
    def getMoveTickRate(self): return alienSpeed
    def getDrawColour(self): 
        if self.row==0: return GREEN
        if self.row == 2: return MAGENTA
        if self.row > 2: return CYAN
        return WHITE
    def calculateXY(self):
        self.y = (invasionLevel * rowSize) + rowSize * startRow + (rowSize * self.row) + (round * rowSize)
        self.x = (currentStep * stepSize) + (colSize) + (colSize * self.col)

    def isBottom(self):
        # returns true if this alien is bottom-most in it's column
        # TODO improve the speed of this by holding isBottom variables? Though it is fast enough.
        if self.state != alive: return False
        for a in o:
            if isinstance(a, Alien) and a.state == alive and a.col == self.col and a.row > self.row: return False
        return True

    def reset(self):
        # mark self as alive
        self.state = alive
        # recalculate xy pos
        self.calculateXY()

    def onHitEvent(self, other):
        Alien.hit_sound.play()
        PixelSprite.onHitEvent(self, other)
        # TODO calculate score based on alien type
        CharacterSurface.addToScore(10)
        # TODO increase alien animation and move speed
        global alienSpeed, speedupRate
        alienSpeed -= speedupRate

    def move(self):
        self.calculateXY()
        # are we the first alien to hit the buffer? If so change direction
        if (self.x > (width - (colSize * 2))) or (self.x < colSize):
            global currentDirection, invasionLevel, currentStep
            currentDirection *= -1
            invasionLevel += 1
            currentStep += currentDirection
            # recalculate
            self.calculateXY()
        # should we fire a shot, are we bottom-most in our column?
        if self.isBottom():
            p = Player.getPlayer()
            if self.isInline(p):
                Shot.fire(self, 1)
            elif random.randint(1, 100) == 1:
                Shot.fire(self, 2)
            elif random.randint(1, 100) == 2:
                Shot.fire(self, 3)
            elif random.randint(1, 100) == 4:
                Shot.fire(self, 4)

    @staticmethod
    def getAlien(row, col):
        for a in o:
            if isinstance(a, Alien) and a.row == row and a.col == col: return a
        na = Alien(row, col)
        o.append(na)
        return na


class Player(PixelSprite):
    def __init__(self):
        PixelSprite.__init__(self, [player1], [playerEx1, playerEx2])
        self.x = width / 2
        self.y = height - (rowSize * 2)
        self.moveStep = 0
        self.setMoveTickRate(2)

    def getDrawColour(self): return GREEN

    def onHitEvent(self, other):
        pass

    def move(self):
        self.x = self.x + self.moveStep
        if self.x < (colSize): self.x = colSize
        if self.x > (width - colSize): self.x = width - colSize
        # TODO check if aliens in line with player and maybe shoot?

    @staticmethod
    def getPlayer():
        for p in o:
            if isinstance(p, Player): return p
        na = Player()
        o.append(na)
        return na


class Saucer(PixelSprite):
    def __init__(self):
        PixelSprite.__init__(self, [saucer1], [saucerExp])
        self.setState(dead)
        self.x = -50
        self.y = rowSize
        self.setMoveTickRate(15)
        self.setAnimationTickRate(25000)
    def getDrawColour(self): return MAGENTA
    def animate(self):
        self.setState(alive)

    def move(self):
        self.x += 2
        if self.x > width + self.width:
            self.setState(dead)
            self.x = -50

    @staticmethod
    def getSaucer():
        for s in o:
            if isinstance(s, Saucer): return s
        na = Saucer()
        o.append(na)
        return na


class Shield(PixelSprite):
    def __init__(self, x):
        PixelSprite.__init__(self, [shield1], [shield1])
        self.xloc = x
        self.backupFrame = self.frames[0]
        self.x = x
        self.y = height - (rowSize * 3.5)
        self.setMoveTickRate(10000000)
        self.setAnimationTickRate(10000000)
    def getDrawColour(self): return GREEN
    def getMask(self): return pygame.mask.from_surface(self.frames[0])

    def erode(self, other):
        # TODO erosion not quite working properly
        # TODO invaders should also erode bases
        ox = other.x - self.x
        oy = other.y - self.y
        m = pygame.mask.from_surface(other.currentlyDisplayedFrame)
        self.frames[0] = pygame.mask.Mask.to_surface(m, surface=self.frames[0], unsetsurface=None, unsetcolor=None, setcolor=TRANSPARENT, dest=(ox, oy))
 
    def onHitEvent(self, other):
        self.setState(alive)
        self.erode(other)

    def reset(self):
        self.frames[0] = self.backupFrame

    @staticmethod
    def getShield(col):
        xloc = col * colSize
        for p in o:
            if isinstance(p, Shield) and p.xloc == xloc: return p
        na = Shield(xloc)
        o.append(na)
        return na

########################################## Game Code
def reset():
    invasionLevel = 1
    currentStep = 0
    currentDirection = right
    currentHeight = 0
    o = []
    player = Player.getPlayer()
    CharacterSurface.initCharacters()
    Saucer.getSaucer()
    Shield.getShield(2)
    Shield.getShield(5)
    Shield.getShield(8)
    Shield.getShield(11)

    for row in range(0, 5):
        for col in range(0, 11):
            a = Alien.getAlien(row, col)
            a.reset()

reset()

lastStepTime = 0
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            p = Player.getPlayer()
            if event.key == pygame.K_LEFT:
                p.moveStep = (-1 * playerSpeed)
            elif event.key == pygame.K_RIGHT:
                p.moveStep = playerSpeed
            elif event.key == pygame.K_SPACE:
                Shot.fire(p, 0)
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                p.moveStep = 0

    if pygame.time.get_ticks() - lastStepTime > alienSpeed:
        lastStepTime = pygame.time.get_ticks()
        currentStep = currentStep + currentDirection
        Alien.move_sounds[currentStep % 4].play()

    screen.fill(BLACK)
    for a in o: a.update()
    CharacterSurface.updateAll()
    pygame.display.update()