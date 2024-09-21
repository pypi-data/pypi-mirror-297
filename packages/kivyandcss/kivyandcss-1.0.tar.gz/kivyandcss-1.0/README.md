kivy-css
kivy-css là một thư viện đơn giản giúp bạn dễ dàng áp dụng các style CSS vào ứng dụng Kivy. Thư viện này cho phép bạn sử dụng cú pháp CSS quen thuộc để thiết kế giao diện, đồng thời hỗ trợ dễ dàng tích hợp vào các dự án Kivy.

Cài đặt
Cài đặt thư viện qua pip:

pip install kivy-css

Sử dụng cơ bản
Dưới đây là một ví dụ cơ bản về cách sử dụng thư viện kivy-css để áp dụng style CSS cho một ứng dụng Kivy.

1. Tạo file style.css
Trước hết, bạn cần tạo file style.css để chứa các style CSS bạn muốn áp dụng. Ví dụ:

#style.css

Label {
    color: red;
    font-size: 24sp;
}

BoxLayout {
    background-color: #B0E57C; /* màu nền xanh nhạt */
}
2. Sử dụng thư viện trong ứng dụng Kivy
Dưới đây là ví dụ về ứng dụng Kivy sử dụng kivy-css để áp dụng các style từ file CSS:

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.graphics import Rectangle, Color
from kivy_css import CssParser  # Import class CssParser từ thư viện kivy-css

class MainApp(App):
    def build(self):
        # Parse CSS và lấy KV styles
        css_parser = CssParser()
        kv_styles = css_parser.parse_file('style.css')
        
        # Load KV styles vào Builder
        Builder.load_string(kv_styles)
        
        # Tạo và trả về widget gốc
        root = BoxLayout()
        
        # Thêm màu nền cho BoxLayout
        with root.canvas.before:
            Color(0.5, 0.5, 0.5, 1)  # Thay đổi màu nền (xám ở đây)
            self.rect = Rectangle(pos=root.pos, size=root.size)
        
        # Liên kết kích thước và vị trí của rectangle với widget gốc
        root.bind(pos=self.update_rect, size=self.update_rect)
        
        header = Label(text='Welcome to My App')
        root.add_widget(header)
        return root
    
    def update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

if __name__ == '__main__':
    MainApp().run()

3. Giải thích mã
CssParser: Đây là lớp chịu trách nhiệm đọc và chuyển đổi các style từ file CSS thành các chuỗi KV mà Kivy có thể hiểu được.
Builder.load_string(kv_styles): Sau khi các style CSS được chuyển thành KV, chúng sẽ được tải vào ứng dụng Kivy để áp dụng.
root.canvas.before: Đoạn mã này sử dụng Kivy.graphics để thêm một màu nền cho BoxLayout trước khi hiển thị các widget con.
Label: Widget Label sẽ nhận style từ file CSS, thay đổi màu chữ thành đỏ và kích thước font thành 24sp.
4. Chạy ứng dụng
Đảm bảo rằng bạn có file style.css trong cùng thư mục với mã Python. Sau đó, chỉ cần chạy ứng dụng:

python main.py
Ứng dụng sẽ khởi động với màu nền cho BoxLayout và style cho Label được áp dụng từ file CSS.