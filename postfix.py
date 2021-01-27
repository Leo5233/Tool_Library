# -*- coding: utf-8 -*-
# 後序法 (a+b)*(c+d) 
# 將原式依運算順序每一層都加上括號 a+b+c --> ((a+b)+c) 一個括弧內只會有一個運算子
# 分前中後三階段 從最左邊一個個取 依序放進中階段
# 如果遇到括號但只有單邊 就一樣放進中階
# 如果取到 +-*/ 將其放進中階 將中階和該運算子同括弧的運算元從右到左 依序移到後階
# 如果遇到括號可湊成一對 將中階的最靠近的括號層的另一邊括號 一整對一起捨棄 括弧的所有東西從右到左 依序移到後階

def priority(op):
# 先*/ 後 +- 最後運算元
    return 1 if op in "+-" else 2 if op in "*/" else 0
    
def toPostfix(infix, isPost = True):
    toStack, toOutput = ('(', ')') if isPost else (')', '(')
    
    def procOpt(c, stack, output):
    # 遇到運算子 
        if stack == "" or priority(stack[-1]) < priority(c):
        # 如果沒有待處理過的 或是 待處理最右一個字元同為運算子(因為有括號湊一對而消失 使運算子相遇)
            return (stack + c, output)
            # 將該放入待處理
        else:
            return procOpt(c, stack[0:-1], output + stack[-1])
            # 不是的話表示待處理最右一個字元為運算元 將其移到output
    
    def procPhs(stack, output):
    # 遇到收尾括號才執行
        if stack[-1] == toStack:
        # 待處理最右一個字元為開頭括號 將開頭括號去掉
            return (stack[0:-1], output)
        else:
        # 待處理最右一個字元若不是開頭括號 則由右到左一一將其移到output
            return procPhs(stack[0:-1], output + stack[-1])
    
    def procExpr(expr, stack = "", output = ""):
    #一個個字元依序處理 三個參數分別為待處理 待處理 最後輸出
        if expr == "": #已經沒有了 或 本來就沒有 將待處理全部移到輸出(由右向左取)
            return output + stack[::-1]
        elif expr[0] == toStack: #如果第一個是左括號 將括號放入待處理
            print(expr[1:], stack + expr[0], output, sep='     ')
            return procExpr(expr[1:], stack + expr[0], output)
        elif expr[0] in "+-*/": # 如果第一個是運算子 將運算子特別處理
            temp = procOpt(expr[0], stack, output)
            print(expr[1:], *temp, sep='     ')
            return procExpr(expr[1:], *procOpt(expr[0], stack, output))
        elif expr[0] == toOutput: #如果第一個是右括號 將括號放入待處理
            temp = procPhs(stack, output)
            print(expr[1:], *temp, sep='     ')
            return procExpr(expr[1:], *procPhs(stack, output))
        else: #如果是運算元 直接放到 output 不用待處理
            print(expr[1:], stack + expr[0], output, sep='     ')
            return procExpr(expr[1:], stack, output + expr[0])
    
    output = procExpr(infix if isPost else infix[::-1])
    return output if isPost else output[::-1]

def toPrefix(infix):
    return toPostfix(infix, False)
    
infix = "(a+b)*(c+d)"
print(toPostfix(infix))
print(toPrefix(infix))