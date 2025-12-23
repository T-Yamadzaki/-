// ------------------------------
// Telegram Mini App Navigation JS
// ------------------------------

// Получаем текущую страницу из data-page в body
const currentPage = document.body.dataset.page;

// Функция для обновления активной кнопки нижнего меню
function setActiveButton(page) {
  document.querySelectorAll(".nav-btn").forEach(btn => {
    btn.classList.remove("active"); // снимаем активность со всех кнопок
    if (btn.dataset.page === page) {
      btn.classList.add("active"); // ставим активной нужную
    }
  });
}

// Сразу при загрузке страницы подсвечиваем активную кнопку
setActiveButton(currentPage);

// Добавляем обработку кликов для всех кнопок нижнего меню
document.querySelectorAll(".nav-btn").forEach(btn => {
  btn.addEventListener("click", () => {
    const page = btn.dataset.page;

    // Меняем активную кнопку при клике
    setActiveButton(page);

    // Лог перехода (позже можно заменить на функцию смены контента или SPA-навигацию)
    console.log("Переход на страницу:", page);
  });
});

// ------------------------------
// Отладка: проверить что JS работает
// ------------------------------
console.log("JS загружен. Текущая страница:", currentPage);
