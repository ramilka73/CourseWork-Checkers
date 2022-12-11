from tkinter import *
from tkinter.messagebox import showinfo, askyesno
import copy

location_x1=-1
chech_move=True

#загруpка картинок шашек
def load_image():
    global checker
    white_checker=PhotoImage(file="wK.png")
    white_checker_queen=PhotoImage(file="wQ.png")
    black_checker=PhotoImage(file="bK.png")
    black_checker_queen=PhotoImage(file="bQ.png")
    checker=[0,white_checker,white_checker_queen,black_checker,black_checker_queen]

#новая игра
def new_game():
    global board_checker
    #растановка шашек в начаое игры
    #0-пустое поле
    #4-черная дамка
    #3-черная шашака
    #2-белая дамка
    #1- белая шашака
    board_checker=[[0,3,0,3,0,3,0,3],[3,0,3,0,3,0,3,0],[0,3,0,3,0,3,0,3],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[1,0,1,0,1,0,1,0],[0,1,0,1,0,1,0,1],[1,0,1,0,1,0,1,0]]


#отрисовка доски с шашками
def draw_board(x1,y1,x2,y2):#рисуем игровое поле
    x=0
    global checker
    global board_checker
    global select_board_canvas,mouse_board_canvas
    #удаляем с канаваса
    board_canvas.delete('all')
    select_board_canvas=board_canvas.create_rectangle(-5, -5, -5, -5,outline="gray",width=5)
    mouse_board_canvas=board_canvas.create_rectangle(-5, -5, -5, -5,outline="gray",width=5)
    
    #масштаб шашаки
    k=50
    
    #рисуем доску
    #четные поля
    while x<8*k:
        y=1*k
        while y<8*k:
            board_canvas.create_rectangle(x, y, x+k, y+k,fill="brown")
            y+=2*k
        x+=2*k
    x=1*k
    
    #не четные поля
    while x<8*k:#рисуем доску
        y=0
        while y<8*k:
            board_canvas.create_rectangle(x, y, x+k, y+k,fill="brown")
            y+=2*k
        x+=2*k
    
    #рисуем шашки
    for y in range(8):
        for x in range(8):
            z=board_checker[y][x]
            if z:  
                if (x1,y1)!=(x,y):#стоячие шашки?
                    board_canvas.create_image(x*k,y*k, anchor=NW, image=checker[z])
    #рисуем активную шашку         
    z=board_checker[y1][x1]
    if z:
        board_canvas.create_image(x1*k,y1*k, anchor=NW, image=checker[z],tag='ani')
    #вычисление коэф. для анимации
    kx = 1 if x1<x2 else -1
    ky = 1 if y1<y2 else -1
    #анимация перемещения шашки
    for i in range(abs(x1-x2)):
        for j in range(33):
            board_canvas.move('ani',0.03*k*kx,0.03*k*ky)
            board_canvas.update()

#движение мышкой по клеткам
def move_mouse(event):
    #опредлеем координаты клетки
    x,y=(event.x)//50,(event.y)//50
    #рамка в выбранной клетке
    board_canvas.coords(mouse_board_canvas,x*50,y*50,x*50+50,y*50+50)

#нажатие на клетку
def click_mouse(event):
    global location_x1,location_y1,location_x2,location_y2
    global chech_move
    x,y=(event.x)//50,(event.y)//50#вычисляем координаты клетки
    #print(x,y),
    #проверяем наличие шашки
    #проверяем шашку в выбранной клетке
    if board_checker[y][x]==1 or board_checker[y][x]==2 or board_checker[y][x]==3 or board_checker[y][x]==4:
        #рисуем рамку
        board_canvas.coords(select_board_canvas,x*50,y*50,x*50+50,y*50+50)
        location_x1,location_y1=x,y
    else:
        #клетка выбрана    
        if location_x1!=-1:
            location_x2,location_y2=x,y
            if chech_move:#ход игрока
                turn_player ()
                if not(chech_move):
                    #если ход сделан проверяем все возможные исходы
                    check_game()
            #клетка не выбрана
            location_x1=-1
            #рамка вне поля
            board_canvas.coords(select_board_canvas,-5,-5,-5,-5)              

#проверка хода игрока
def turn_player ():
    global location_x1,location_y1,location_x2,location_y2
    global chech_move
    #ход произведен
    chech_move=False
    #создаем список возможных ходов для игроков
    list_white=list_one()
    list_black=list_two()
        
    #провеяем ход на возможность
    if list_white and list_black:
        #для белых проверяем ход на соответствие правилам игры
        if ((location_x1,location_y1),(location_x2,location_y2)) in list_white:
            #делаем ход
            do_move=turn_checkers(1,location_x1,location_y1,location_x2,location_y2)            
            #есть ещё ход этой шашкой
            if do_move:
                #ход невыполнен
                chech_move=True
        #для черных проверяем ход на соответствие правилам игры        
        elif ((location_x1,location_y1),(location_x2,location_y2)) in list_black:
            #делаем ход    
            do_move=turn_checkers(1,location_x1,location_y1,location_x2,location_y2)        
            #есть ещё ход этой шашкой
            if do_move:#если есть ещё ход той же шашкой
                #ход невыполнен
                chech_move=True              
        else:
            #ход невыполнен
            chech_move=True
    board_canvas.update()

#проверка исходов игры   
def check_game():#!!!
    global chech_move
    chech_move=True
    #определяем победителя 
    result_white,result_black=check_checkers()
    if not(result_black):
            end_game(2)
    elif not(result_white):
            end_game(1)
    elif chech_move and not(list_one()):
            end_game(3)
    elif not(chech_move) and not(list_two()):
            end_game(3)
            
#список ходов черными
def list_two():
    #обязательные ходы
    list_white=check_mandatory_moves_black([])
    if not(list_white):
        #проверяем оставшиеся ходы
        list_white=check_last_moves_black([])
    return list_white

#список ходов белыми
def list_one():
    #обязательные ходы
    list_white=check_mandatory_moves_white([])
    if not(list_white):
        #проверяем оставшиеся ходы
        list_white=check_last_moves_white([])
    return list_white
    

#проверка шашек на поле
def check_checkers():
    global board_checker
    result_black=0
    result_white=0
    for i in range(8):
        for j in board_checker[i]:
            if j==1:result_black+=1
            if j==2:result_black+=3
            if j==3:result_white+=1
            if j==4:result_white+=3
    return result_white,result_black

#меняем положение шашки и если надо её тип 
def turn_checkers(f,location_x1,location_y1,location_x2,location_y2):
    global board_checker
    if f:
        draw_board(location_x1,location_y1,location_x2,location_y2)#рисуем игровое поле

    #превращение
    if location_y2==0 and board_checker[location_y1][location_x1]==1:
        board_checker[location_y1][location_x1]=2

    #превращение
    if location_y2==7 and board_checker[location_y1][location_x1]==3:
        board_checker[location_y1][location_x1]=4

    #делаем ход           
    board_checker[location_y2][location_x2]=board_checker[location_y1][location_x1]
    board_checker[location_y1][location_x1]=0

    #забираем шашку
    kx=ky=1
    if location_x1<location_x2:kx=-1
    if location_y1<location_y2:ky=-1
    x_poz,y_poz=location_x2,location_y2
    while (location_x1!=x_poz) or (location_y1!=y_poz):
        x_poz+=kx
        y_poz+=ky
        if board_checker[y_poz][x_poz]!=0:
            board_checker[y_poz][x_poz]=0
            if f:draw_board(-1,-1,-1,-1)#рисуем игровое поле
            #проверяем ход той же шашкой для черных
            if board_checker[location_y2][location_x2]==3 or board_checker[location_y2][location_x2]==4:
                #возвращаем список доступных ходов
                return check_mandatory_moves_blackp([],location_x2,location_y2)
            #проверяем ход той же шашкой для белых
            elif board_checker[location_y2][location_x2]==1 or board_checker[location_y2][location_x2]==2:
                #возвращаем список доступных ходов
                return check_mandatory_moves_whitep([],location_x2,location_y2)
    if f:draw_board(location_x1,location_y1,location_x2,location_y2)#рисуем игровое поле

#проверка наличия обязательных ходов
def check_mandatory_moves_black(list_white):
    for y in range(8):#сканируем всё поле
        for x in range(8):
            list_white=check_mandatory_moves_blackp(list_white,x,y)
    return list_white

#проверка наличия обязательных ходов
def check_mandatory_moves_blackp(list_white,x,y):
    if board_checker[y][x]==3:
        for new_x,new_y in (-1,-1),(-1,1),(1,-1),(1,1):
            if 0<=y+new_y+new_y<=7 and 0<=x+new_x+new_x<=7:
                if board_checker[y+new_y][x+new_x]==1 or board_checker[y+new_y][x+new_x]==2:
                    if board_checker[y+new_y+new_y][x+new_x+new_x]==0:
                        list_white.append(((x,y),(x+new_x+new_x,y+new_y+new_y)))#запись хода в конец списка
    if board_checker[y][x]==4:#шашка с короной
        for new_x,new_y in (-1,-1),(-1,1),(1,-1),(1,1):
            error=0#определение правильности хода
            for i in  range(1,8):
                if 0<=y+new_y*i<=7 and 0<=x+new_x*i<=7:
                    if error==1:
                        list_white.append(((x,y),(x+new_x*i,y+new_y*i)))#запись хода в конец списка
                    if board_checker[y+new_y*i][x+new_x*i]==1 or board_checker[y+new_y*i][x+new_x*i]==2:
                        error+=1
                    if board_checker[y+new_y*i][x+new_x*i]==3 or board_checker[y+new_y*i][x+new_x*i]==4 or error==2:
                        if error>0:list_white.pop()#удаление хода из списка
                        break
    return list_white

#проверка наличия остальных ходов
def check_last_moves_black(list_white):
    for y in range(8):
        for x in range(8):
            if board_checker[y][x]==3:
                for new_x,new_y in (-1,1),(1,1):
                    if 0<=y+new_y<=7 and 0<=x+new_x<=7:
                        if board_checker[y+new_y][x+new_x]==0:
                            list_white.append(((x,y),(x+new_x,y+new_y)))
                        if board_checker[y+new_y][x+new_x]==1 or board_checker[y+new_y][x+new_x]==2:
                            if 0<=y+new_y*2<=7 and 0<=x+new_x*2<=7:
                                if board_checker[y+new_y*2][x+new_x*2]==0:
                                    list_white.append(((x,y),(x+new_x*2,y+new_y*2)))               
            if board_checker[y][x]==4:#шашка с короной
                for new_x,new_y in (-1,-1),(-1,1),(1,-1),(1,1):
                    error=0#определение правильности хода
                    for i in range(1,8):
                        if 0<=y+new_y*i<=7 and 0<=x+new_x*i<=7:
                            if board_checker[y+new_y*i][x+new_x*i]==0:
                                list_white.append(((x,y),(x+new_x*i,y+new_y*i)))#запись хода в конец списка
                            if board_checker[y+new_y*i][x+new_x*i]==1 or board_checker[y+new_y*i][x+new_x*i]==2:
                                error+=1
                            if board_checker[y+new_y*i][x+new_x*i]==3 or board_checker[y+new_y*i][x+new_x*i]==4 or error==2:
                                break
    return list_white
    
#проверка наличия обязательных ходов
def check_mandatory_moves_white(list_white):
    list_white=[]#список ходов
    for y in range(8):#сканируем всё поле
        for x in range(8):
            list_white=check_mandatory_moves_whitep(list_white,x,y)
    return list_white

#проверка наличия обязательных ходов
def check_mandatory_moves_whitep(list_white,x,y):
    if board_checker[y][x]==1:#шашка
        for new_x,new_y in (-1,-1),(-1,1),(1,-1),(1,1):
            if 0<=y+new_y+new_y<=7 and 0<=x+new_x+new_x<=7:
                if board_checker[y+new_y][x+new_x]==3 or board_checker[y+new_y][x+new_x]==4:
                    if board_checker[y+new_y+new_y][x+new_x+new_x]==0:
                        list_white.append(((x,y),(x+new_x+new_x,y+new_y+new_y)))
    if board_checker[y][x]==2:#шашка с короной
        for new_x,new_y in (-1,-1),(-1,1),(1,-1),(1,1):
            error=0#определение правильности хода
            for i in  range(1,8):
                if 0<=y+new_y*i<=7 and 0<=x+new_x*i<=7:
                    if error==1:
                        list_white.append(((x,y),(x+new_x*i,y+new_y*i)))#запись хода в конец списка
                    if board_checker[y+new_y*i][x+new_x*i]==3 or board_checker[y+new_y*i][x+new_x*i]==4:
                        error+=1
                    if board_checker[y+new_y*i][x+new_x*i]==1 or board_checker[y+new_y*i][x+new_x*i]==2 or error==2:
                        if error>0:list_white.pop()#удаление хода из списка
                        break
    return list_white
#проверка наличия остальных ходов
def check_last_moves_white(list_white):
    for y in range(8):
        for x in range(8):
            if board_checker[y][x]==1:#шашка
                for new_x,new_y in (-1,-1),(1,-1):
                    if 0<=y+new_y<=7 and 0<=x+new_x<=7:
                        if board_checker[y+new_y][x+new_x]==0:
                            list_white.append(((x,y),(x+new_x,y+new_y)))#запись хода в конец списка
                        if board_checker[y+new_y][x+new_x]==3 or board_checker[y+new_y][x+new_x]==4:
                            if 0<=y+new_y*2<=7 and 0<=x+new_x*2<=7:
                                if board_checker[y+new_y*2][x+new_x*2]==0:
                                    list_white.append(((x,y),(x+new_x*2,y+new_y*2)))#запись хода в конец списка                  
            if board_checker[y][x]==2:#шашка с короной
                for new_x,new_y in (-1,-1),(-1,1),(1,-1),(1,1):
                    error=0#определение правильности хода
                    for i in range(1,8):
                        if 0<=y+new_y*i<=7 and 0<=x+new_x*i<=7:
                            if board_checker[y+new_y*i][x+new_x*i]==0:
                                list_white.append(((x,y),(x+new_x*i,y+new_y*i)))#запись хода в конец списка
                            if board_checker[y+new_y*i][x+new_x*i]==3 or board_checker[y+new_y*i][x+new_x*i]==4:
                                error+=1
                            if board_checker[y+new_y*i][x+new_x*i]==1 or board_checker[y+new_y*i][x+new_x*i]==2 or error==2:
                                break
    return list_white

#конец игры
def end_game(s):
    global chech_move
    if s==1:
        i=askyesno(title='Игра завершена', message='Белые победили!\nНажми "Да" что бы начать заново.',icon='info')
    if s==2:
        i=askyesno(title='Игра завершена', message='Черные победили!\nНажми "Да" что бы начать заново.',icon='info')
    if s==3:
        i=askyesno(title='Игра завершена', message='Ходов больше нет.\nНажми "Да" что бы начать заново.',icon='info')
    if i:
        new_game()
        #рисуем игровое поле
        draw_board(-1,-1,-1,-1)
        chech_move=True

#создаём окно
game_window=Tk()
#указываем заголовок окна
game_window.title('Ставропольские шашки')
#создадим конву для игры
board_canvas=Canvas(game_window, width=400,height=400,bg='#EEEEDD')
board_canvas.pack()
#загружаем изображения шашек
load_image()
#начинаем новую игру
new_game()
#рисуем игровое поле
draw_board(-1,-1,-1,-1)
#перемещение курсора мыши
board_canvas.bind("<Motion>", move_mouse)
#нажатие ЛКМ
board_canvas.bind("<Button-1>", click_mouse)
mainloop()
