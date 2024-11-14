const questions = [
    // Открытость опыту
    { text: "Мне нравится узнавать новое и пробовать необычные вещи.", category: "openness" },
    { text: "Меня привлекают творческие или интеллектуальные занятия.", category: "openness" },
    { text: "Я часто ищу новые идеи и подходы.", category: "openness" },
    { text: "Я любопытен и открыт к новому опыту.", category: "openness" },
    { text: "Я считаю важным иметь нестандартный взгляд на мир.", category: "openness" },
    { text: "Меня вдохновляют философские или глубокие размышления.", category: "openness" },
    { text: "Я считаю себя творческой личностью.", category: "openness" },
    { text: "Я легко представляю альтернативные подходы к решению проблем.", category: "openness" },
    { text: "Меня привлекают необычные или сложные темы.", category: "openness" },
    { text: "Я люблю изучать новые культуры и традиции.", category: "openness" },

    // Добросовестность
    { text: "Я всегда довожу начатое до конца.", category: "conscientiousness" },
    { text: "Я организован и аккуратен в своих делах.", category: "conscientiousness" },
    { text: "Я предпочитаю работать по четкому плану.", category: "conscientiousness" },
    { text: "Я считаю важным быть надежным и ответственным.", category: "conscientiousness" },
    { text: "Я стараюсь всегда следовать намеченным целям.", category: "conscientiousness" },
    { text: "Мне важно чувствовать, что я контролирую свои задачи.", category: "conscientiousness" },
    { text: "Я ответственно отношусь к своим обязанностям.", category: "conscientiousness" },
    { text: "Я редко откладываю дела на потом.", category: "conscientiousness" },
    { text: "Я предпочитаю планировать свои действия заранее.", category: "conscientiousness" },
    { text: "Я настойчив и последователен в достижении целей.", category: "conscientiousness" },

    // Экстраверсия
    { text: "Мне нравится быть в центре внимания.", category: "extraversion" },
    { text: "Я люблю общаться и заводить новых друзей.", category: "extraversion" },
    { text: "Я чувствую прилив энергии при взаимодействии с другими людьми.", category: "extraversion" },
    { text: "Я чувствую себя уверенно в больших группах.", category: "extraversion" },
    { text: "Я предпочитаю активный образ жизни.", category: "extraversion" },
    { text: "Я легко завожу разговоры с незнакомыми людьми.", category: "extraversion" },
    { text: "Я люблю быть частью крупных мероприятий.", category: "extraversion" },
    { text: "Я ощущаю прилив сил, когда нахожусь в компании.", category: "extraversion" },
    { text: "Я охотно беру на себя лидерские роли.", category: "extraversion" },
    { text: "Я чувствую себя комфортно в публичных ситуациях.", category: "extraversion" },

    // Доброжелательность
    { text: "Мне нравится поддерживать других и оказывать помощь.", category: "agreeableness" },
    { text: "Я стремлюсь к гармоничным отношениям с окружающими.", category: "agreeableness" },
    { text: "Мне важно, чтобы люди вокруг меня были довольны.", category: "agreeableness" },
    { text: "Я всегда готов к компромиссу ради мира и спокойствия.", category: "agreeableness" },
    { text: "Я стремлюсь понять чувства и мысли других людей.", category: "agreeableness" },
    { text: "Я легко доверяю окружающим и охотно делюсь с ними.", category: "agreeableness" },
    { text: "Я предпочитаю сотрудничество, а не соперничество.", category: "agreeableness" },
    { text: "Мне важно быть терпимым и понимать других.", category: "agreeableness" },
    { text: "Я чувствую удовлетворение, когда помогаю другим.", category: "agreeableness" },
    { text: "Я стараюсь быть внимательным к нуждам окружающих.", category: "agreeableness" },

    // Нейротизм
    { text: "Я часто беспокоюсь о различных мелочах.", category: "neuroticism" },
    { text: "Меня легко выбить из состояния равновесия.", category: "neuroticism" },
    { text: "Я склонен к эмоциональным перепадам.", category: "neuroticism" },
    { text: "Мне сложно справляться со стрессовыми ситуациями.", category: "neuroticism" },
    { text: "Я легко поддаюсь негативным эмоциям.", category: "neuroticism" },
    { text: "Я часто чувствую беспокойство или тревогу.", category: "neuroticism" },
    { text: "Я часто чувствую себя неуверенно.", category: "neuroticism" },
    { text: "Мне сложно сохранять спокойствие в напряженных ситуациях.", category: "neuroticism" },
    { text: "Я чувствую себя уязвимым и подверженным стрессу.", category: "neuroticism" },
    { text: "Я склонен к самокритике и беспокойству.", category: "neuroticism" }
];

// Переменные для отслеживания текущего вопроса и результатов
let currentQuestion = 0;
const answers = {
    openness: 0,
    conscientiousness: 0,
    extraversion: 0,
    agreeableness: 0,
    neuroticism: 0
};

function startTest() {
    document.getElementById("welcome-container").classList.add("hidden");
    document.getElementById("question-container").classList.remove("hidden");
    showQuestion();
}

function showQuestion() {
    document.getElementById("question-text").textContent = questions[currentQuestion].text;
}

function nextQuestion() {
    const selectedAnswer = document.querySelector('input[name="answer"]:checked');
    if (!selectedAnswer) {
        alert("Выберите вариант ответа, чтобы продолжить!");
        return;
    }
    
    answers[questions[currentQuestion].category] += parseInt(selectedAnswer.value);
    selectedAnswer.checked = false;
    currentQuestion++;

    if (currentQuestion < questions.length) {
        showQuestion();
    } else {
        showResults();
    }
}

function showResults() {
    document.getElementById("question-container").classList.add("hidden");
    document.getElementById("result-container").classList.remove("hidden");

    const resultText = generateInterpretation();
    document.getElementById("result-text").innerHTML = resultText;
}

function generateInterpretation() {
    const interpretations = {
        openness: { /* добавьте развернутые описания для openness */ },
        conscientiousness: { /* добавьте развернутые описания для conscientiousness */ },
        extraversion: { /* добавьте развернутые описания для extraversion */ },
        agreeableness: { /* добавьте развернутые описания для agreeableness */ },
        neuroticism: { /* добавьте развернутые описания для neuroticism */ }
    };

    const resultStrings = [];

    for (const category in answers) {
        let score = answers[category];
        let interpretation = "";

        if (score > 30) {
            interpretation = interpretations[category].high;
        } else if (score > 20) {
            interpretation = interpretations[category].medium;
        } else {
            interpretation = interpretations[category].low;
        }

        resultStrings.push(interpretation);
    }

    return resultStrings.join("<br><br>");
}

function restartTest() {
    currentQuestion = 0;
    for (const category in answers) {
        answers[category] = 0;
    }
    document.getElementById("result-container").classList.add("hidden");
    document.getElementById("welcome-container").classList.remove("hidden");
}
