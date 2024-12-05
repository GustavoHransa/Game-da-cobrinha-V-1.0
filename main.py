import sys
import random
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QLabel
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QPainter, QColor, QPixmap,QFont

class JanelaInicial(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('inicial.ui', self)  
       
        self.pushButton.clicked.connect(self.abrir_cobrinha)
        self.background_image = QPixmap('snake.jpg') 

    def abrir_cobrinha(self):
        self.cobrinha = JanelaCobrinha()  
        self.cobrinha.show() 
        self.close()  

class JanelaCobrinha(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('cobrinha.ui', self)  

        # Initialize game variables
        self.snake = [(100, 100), (90, 100), (80, 100)]
        self.direction = Qt.Key_Right
        self.food = self.place_food()
        self.score = 0  
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_game)
        self.timer.start(100)  

     
        self.background_image = QPixmap('fundo.jpg')  

       
        self.score_label = QLabel(self)
        self.score_label.setGeometry(10, 10, 100, 30)  
        self.update_score_display() 
        font = QFont("Arial", 20) 
        self.score_label.setFont(font)

        
        self.score_label.setStyleSheet("color: white;") 


    def place_food(self):
        x = random.randint(0, 59) * 10
        y = random.randint(0, 39) * 10
        return (x, y)

    def update_game(self):
        head_x, head_y = self.snake[0]
        if self.direction == Qt.Key_Right:
            head_x += 10
        elif self.direction == Qt.Key_Left:
            head_x -= 10
        elif self.direction == Qt.Key_Up:
            head_y -= 10
        elif self.direction == Qt.Key_Down:
            head_y += 10

      
        if head_x < 0 or head_x >= self.width() or head_y < 0 or head_y >= self.height():
            self.game_over()
            return

       
        if (head_x, head_y) in self.snake:
            self.game_over()
            return

        self.snake.insert(0, (head_x, head_y))
        if (head_x, head_y) == self.food:
            self.food = self.place_food()  
            self.score += 1 
            self.update_score_display() 
        else:
            self.snake.pop()  

        self.update() 

    def update_score_display(self):
        self.score_label.setText(f"Score: {self.score}") 

    def paintEvent(self, event):
        painter = QPainter(self)

       
        painter.drawPixmap(0, 0, self.background_image.scaled(self.size(), Qt.KeepAspectRatioByExpanding))

      
        for segment in self.snake:
            painter.fillRect(segment[0], segment[1], 10, 10, QColor(0, 255, 0))  

      
        painter.fillRect(self.food[0], self.food[1], 10, 10, QColor(255, 0, 0)) 
    def keyPressEvent(self, event):
            if (event.key() == Qt.Key_Up and self.direction != Qt.Key_Down) or \
               (event.key() == Qt.Key_Down and self.direction != Qt.Key_Up) or \
               (event.key() == Qt.Key_Left and self.direction != Qt.Key_Right) or \
               (event.key() == Qt.Key_Right and self.direction != Qt.Key_Left):
                self.direction = event.key() 

    def game_over(self):
        self.timer.stop()  
        reply = QMessageBox.question(self, "Game Over", "Você perdeu! Deseja jogar novamente?", 
                                      QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.restart_game()  
        else:
            self.close() 

    def restart_game(self):
        self.snake = [(100, 100), (90, 100), (80, 100)]  
        self.direction = Qt.Key_Right  
        self.food = self.place_food()  
        self.score = 0 
        self.update_score_display() 
        self.timer.start(100)  

if __name__ == '__main__':
    app = QApplication(sys.argv)
    janela_inicial = JanelaInicial()  
    janela_inicial.show() 
    sys.exit(app.exec_())  