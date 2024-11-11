from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
import json

# создаем словарик с заметками
# notes_dir = {
#     'Добро пожаловать':{
#         'текст': 'Лучшие заметки года!',

#         'теги': ['заметки' , 'лучшие']
#     }
# }

# запись в json файл
# with open('f.json' , 'w' , encoding= 'utf-8') as file:
    # json.dump(notes_dir , file)

# чтение файла
with open('f.json' , 'r' , encoding= 'utf-8') as file:
    date = json.load(file)

# создаем функцию обратботчик
def show_note():
    name = notes.selectedItems()[0].text()
    text_field.setText(date[name]['текст'])
    tags.clear()
    tags.addItems(date[name]['теги'])    

app = QApplication([])
main_win = QWidget()
main_win.setWindowTitle('Умные заметки')
main_win.resize(1100 , 1000)

# создаем виджеты - кнопки
create_b = QPushButton('Создать заметку')
delete_b = QPushButton('удалить заметку')
save_b = QPushButton('Сохранить заметку')

app_b = QPushButton('Добавить к заметке')
unpin_b = QPushButton('Открепить от заметки')
seek_b = QPushButton('Искать заметки по тегу')

# создаем виджеты - списки
notes = QListWidget()
tags = QListWidget()

# создаем виджеты - поиск тегов
seek_tegs = QLineEdit()

# создаем виджеты - текстовое поле
text_field = QTextEdit()

# создаем виджеты - текст для списков
label_notes = QLabel('Список заметок')
label_tags = QLabel('Список тегов')


# создаем линии для виджетов
layt_text = QVBoxLayout()
layt_widget = QVBoxLayout()
layt_for_nots = QHBoxLayout()
layt_for_tags = QHBoxLayout()
layt_Hmain = QHBoxLayout()

# закидываем виджеты на линии
layt_text.addWidget(text_field) 

layt_widget.addWidget(label_notes)
layt_widget.addWidget(notes)
layt_for_nots.addWidget(create_b)
layt_for_nots.addWidget(delete_b)
layt_widget.addLayout(layt_for_nots)
layt_for_tags.addWidget(app_b)
layt_for_tags.addWidget(unpin_b)
layt_widget.addWidget(save_b)

layt_widget.addWidget(label_tags)
layt_widget.addWidget(tags)
layt_widget.addWidget(seek_tegs)
layt_widget.addLayout(layt_for_tags)
layt_widget.addWidget(seek_b)

layt_Hmain.addLayout(layt_text)
layt_Hmain.addLayout(layt_widget)

notes.addItems(date)

# Применяем получившийся лэйаут к окну приложения
main_win.setLayout(layt_Hmain)

# обработчики кнопок
def add_note():
    note_name, result = QInputDialog.getText(main_win, 'Добавить заметку', 'Название заметки:')
    if note_name != '' and result == True:
        date[note_name] = {'текст': '', 'теги': []}
        notes.addItem(note_name)
        tags.addItems(date[note_name]['теги'])

def del_note():
    if notes.selectedItems():
        name_note = notes.selectedItems()[0].text()

        del date[name_note]
        notes.clear()
        tags.clear()
        text_field.clear()

        notes.addItems(date)

        with open('f.json' , 'w' , encoding= 'utf-8') as file:
            json.dump(date, file)

def save_note():
    if notes.selectedItems():
        text = text_field.toPlainText()
        name_note = notes.selectedItems()[0].text()
        date[name_note]['текст'] = text
        with open('f.json' , 'w' , encoding= 'utf-8') as file:
            json.dump(date, file)

# подключаем кнопки обработчики
create_b.clicked.connect(add_note)
delete_b.clicked.connect(del_note)
save_b.clicked.connect(save_note)

# обработчики кнопок теги
def add_tag():
    if notes.selectedItems(): 
        tag = seek_tegs.text()
        name_note = notes.selectedItems()[0].text()

        if tag not in date[name_note]['теги']:
            date[name_note]['теги'].append(tag)
            tags.addItem(tag)
            seek_tegs.clear()

            with open('f.json' , 'w' , encoding= 'utf-8') as file:
                json.dump(date, file)

def del_tag():
    if notes.selectedItems(): 
        name_note = notes.selectedItems()[0].text()
        if tags.selectedItems(): 
            name_tag = tags.selectedItems()[0].text()
            tags.clear()
            date[name_note]['теги'].remove(name_tag)
            
            tags.addItems(date[name_note]['теги'])

            with open('f.json' , 'w' , encoding= 'utf-8') as file:
                json.dump(date, file)

def search_tag():
    tag = seek_tegs.text()
    if tag and seek_b.text() == 'Искать заметки по тегу':
        names_note = []
        for key in date:
            if tag in date[key]['теги']:
                names_note.append(key)

        notes.clear()
        text_field.clear()
        tags.clear()

        notes.addItems(names_note)
        seek_b.setText('Сбросить поиск')

    elif seek_b.text() == 'Сбросить поиск':
        seek_tegs.clear()
        notes.clear()
        text_field.clear()
        tags.clear()

        notes.addItems(date)
        seek_b.setText('Искать заметки по тегу')


# подключаем обработчики кнопок теги
app_b.clicked.connect(add_tag)
unpin_b.clicked.connect(del_tag)
seek_b.clicked.connect(se)



notes.itemClicked.connect(show_note)
main_win.show()
app.exec_()
