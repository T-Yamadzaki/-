<?php
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Получаем данные из формы
    $name = htmlspecialchars(trim($_POST['name']));
    $email = htmlspecialchars(trim($_POST['email']));
    $message = htmlspecialchars(trim($_POST['message']));

    // Проверка, что все поля заполнены
    if (!empty($name) && !empty($email) && !empty($message)) {
        // Здесь можно добавить код для отправки данных на email или в базу данных

        // Вывод сообщения об успешной отправке
        echo "<h2>Спасибо, $name! Ваше сообщение успешно отправлено.</h2>";
        echo "<p><strong>Имя:</strong> $name</p>";
        echo "<p><strong>Email:</strong> $email</p>";
        echo "<p><strong>Сообщение:</strong> $message</p>";

        // Кнопка для возврата на предыдущую страницу
        echo '<p><a href="index.html">Вернуться на главную</a></p>';
    } else {
        echo "<h2>Ошибка! Все поля должны быть заполнены.</h2>";
        echo '<p><a href="index.html">Попробовать снова</a></p>';
    }
} else {
    echo "<h2>Неверный метод отправки формы!</h2>";
}
?>
