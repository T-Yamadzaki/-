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

const currentPage = document.body.dataset.page;

document.querySelectorAll(".nav-btn").forEach(btn => {
  const page = btn.dataset.page;

  // сбрасываем активность
  btn.classList.remove("active");

  // если совпадает — делаем активной
  if (page === currentPage) {
    btn.classList.add("active");
  }

  // обработчик клика (на будущее)
  btn.addEventListener("click", () => {
    console.log("Переход:", page);
  });
});


