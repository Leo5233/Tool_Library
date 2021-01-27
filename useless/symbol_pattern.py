import random 
main = ['. ','` ','˙','。 ','  ','˚','ˇ','ˆ','˟','ː', 'ׄ ׅ,','॰','ॱ' ,'౦', '˟', '྆', '༶','༙','ᐪ','ᐣ','ᐢ','ᑊ' ,'⭐','ⱃ']*2
big = ['-', '*','^','༡','ᄼ','ᄋ','ᐊ','ᐁ','ᐖ','ᕳ','ᕵ','ᕺ','⭐','Ⱌ','ⱶ','ⵢ']
white = [' ']*75
x = main + big + white

for i in range(35):
    for j in range(35):
        print(random.choice(x), end = ' ')
    print()
    

# for i in range(7500,8500):
#     print(chr(i),end = ', ')