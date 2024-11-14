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

let currentQuestion = 0;
const answers = {
    openness: 0,
    conscientiousness: 0,
    extraversion: 0,
    agreeableness: 0,
    neuroticism: 0
};



function startTest() {
    // Скрываем экран приветствия и показываем вопросы
    document.getElementById("welcome-container").classList.add("hidden");
    document.getElementById("question-container").classList.remove("hidden");

    // Поменяем текст на первый вопрос
    showQuestion();
    // Меняем текст на кнопке на "Следующий вопрос"
    document.getElementById("start-button").style.display = "none";
    document.getElementById("next-button").style.display = "inline-block";
}

function showQuestion() {
    const question = questions[currentQuestion];
    document.getElementById("question-text").textContent = question.text;
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
    // Скрываем вопросы и показываем результаты
    document.getElementById("question-container").classList.add("hidden");
    document.getElementById("result-container").classList.remove("hidden");

    const resultText = generateInterpretation();
    document.getElementById("result-text").innerHTML = resultText;
}

function generateInterpretation() {
    const interpretations = {
              openness: {
            low: "Открытость опыту: Вы менее склонны к поиску новых впечатлений и идей. Вам может быть комфортнее с привычными методами и распорядками, что помогает сохранять стабильность. Рекомендация: попробуйте открываться новым идеям, это может дать вдохновение и свежие перспективы.",
            medium: "Открытость опыту: Вы открыты к новому, но в пределах комфортного. Вам нравятся разнообразие и новые идеи, но вы не всегда склонны к экспериментам. Рекомендация: иногда позволяйте себе рисковать и пробовать что-то новое, это может расширить ваши горизонты.",
            high: "Открытость опыту: Вы активно стремитесь к новым идеям и впечатлениям. Вы творческая личность, обладающая богатым воображением и способностью находить необычные решения. Рекомендация: продолжайте развивать свою открытость, это поможет вам оставаться креативным и вдохновленным."
        },
        conscientiousness: {
            low: "Добросовестность: У вас менее выражена склонность к организованности и целеустремленности. Вы можете быть гибким и быстро адаптироваться, но иногда вам не хватает последовательности. Рекомендация: старайтесь больше планировать задачи и держаться поставленных целей.",
            medium: "Добросовестность: Вы стремитесь к организованности и ответственности, но не всегда следуете строгим правилам. Это позволяет вам сохранять баланс между структурой и гибкостью. Рекомендация: определите ключевые задачи и придерживайтесь их для большей продуктивности.",
            high: "Добросовестность: Вы очень организованный и ответственный человек. Вы всегда доводите дела до конца и строго следуете поставленным целям. Рекомендация: используйте свою организованность для достижения более амбициозных целей и улучшения своей дисциплины."
        },
        extraversion: {
            low: "Экстраверсия: Вы более склонны к уединению и предпочитаете спокойные ситуации. Вам не всегда комфортно в больших группах и публичных мероприятиях. Рекомендация: поддерживайте баланс между временем в одиночестве и общением с другими, это поможет сохранить энергию.",
            medium: "Экстраверсия: Вам нравится быть среди людей, но вы не всегда стремитесь к этому. Вы сохраняете баланс между общительностью и временем для себя. Рекомендация: попробуйте развивать свои социальные навыки, это может быть полезно в построении контактов.",
            high: "Экстраверсия: Вы энергичный и общительный человек, которому нравится быть в центре внимания. Вы легко находите общий язык с людьми и заряжаете их энергией. Рекомендация: используйте свою экстраверсию для укрепления связей и новых возможностей."
        },
        agreeableness: {
            low: "Доброжелательность: Вы предпочитаете соблюдать дистанцию в общении и больше ориентированы на собственные интересы. Иногда это позволяет сохранять независимость, но может затруднять сотрудничество. Рекомендация: попробуйте больше слушать других и искать компромиссы для улучшения общения.",
            medium: "Доброжелательность: Вы умеете поддерживать хорошие отношения с людьми, но при этом не теряете себя. Вам комфортно помогать другим, но вы не позволяете людям злоупотреблять вашей добротой. Рекомендация: продолжайте развивать свои социальные навыки и доброжелательность.",
            high: "Доброжелательность: Вы очень отзывчивый и эмпатичный человек. Вам нравится поддерживать и помогать другим, а также создавать гармонию в отношениях. Рекомендация: сохраняйте баланс между заботой о других и заботой о себе."
        },
        neuroticism: {
            low: "Нейротизм: Вы эмоционально устойчивы и легко справляетесь со стрессом. Вас сложно выбить из равновесия, что позволяет сохранять спокойствие в сложных ситуациях. Рекомендация: используйте свою устойчивость для поддержки других людей, которые нуждаются в этом.",
            medium: "Нейротизм: Вы можете испытывать беспокойство или стресс в сложных ситуациях, но в целом умеете справляться с эмоциями. Вам удается находить баланс между спокойствием и чувствительностью. Рекомендация: развивайте методы управления стрессом, чтобы улучшить свою эмоциональную устойчивость.",
            high: "Нейротизм: Вы чувствительны к стрессу и легко поддаетесь эмоциям. Это может создавать трудности в напряженных ситуациях. Рекомендация: постарайтесь освоить техники релаксации и управления стрессом, это поможет вам лучше контролировать свои эмоции."
        }
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

        resultStrings.push(`<b>${category.charAt(0).toUpperCase() + category.slice(1)}</b>: ${interpretation}`);
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
    document.getElementById("start-button").style.display = "inline-block"; // Показать кнопку Старт
    document.getElementById("next-button").style.display = "none"; // Скрыть кнопку "Следующий вопрос"
}
