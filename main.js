const tg = window.Telegram.WebApp;
const user = tg.initDataUnsafe.user || {first_name: "Гость"};

document.getElementById("horoscope")?.addEventListener("click", () => {
    alert(`Привет, ${user.first_name}! Здесь будет твой гороскоп.`);
});

document.getElementById("compatibility")?.addEventListener("click", () => {
    alert(`Привет, ${user.first_name}! Здесь будет проверка совместимости.`);
});

document.getElementById("forecast")?.addEventListener("click", () => {
    alert(`Привет, ${user.first_name}! Здесь будет прогноз на месяц/год.`);
});

document.getElementById("subscription")?.addEventListener("click", () => {
    alert(`Привет, ${user.first_name}! Здесь будет страница подписки.`);
});

document.getElementById("profile")?.addEventListener("click", () => {
    alert(`Открываю профиль пользователя ${user.first_name}.`);
});

document.getElementById("support")?.addEventListener("click", () => {
    alert("Свяжитесь с нами: support@example.com");
});

// Определяем текущую страницу из body
const currentPage = document.body.dataset.page;

// Функция для обновления активной кнопки
function setActiveButton(page) {
  document.querySelectorAll(".nav-btn").forEach(btn => {
    btn.classList.remove("active"); // убираем со всех
    if (btn.dataset.page === page) {
      btn.classList.add("active"); // ставим активной нужную
    }
  });
}

// Сразу при загрузке ставим активную кнопку
setActiveButton(currentPage);

// Обработчик кликов (на будущее)
document.querySelectorAll(".nav-btn").forEach(btn => {
  btn.addEventListener("click", () => {
    const page = btn.dataset.page;
    setActiveButton(page);
    console.log("Переход:", page);
    // Здесь можно добавить переход на другую страницу
  });
});



