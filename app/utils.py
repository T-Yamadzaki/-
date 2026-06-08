from datetime import datetime, timezone


def parse_product_text(text: str) -> tuple[str, str]:
    parts = text.split("#", 1)
    if len(parts) < 2:
        article = text.split()[0] if text.split() else ""
        return article, ""

    article = parts[0].strip()
    rest = parts[1]

    if "#" in rest:
        size = rest.split("#")[0].strip()
    else:
        size = rest.strip().split()[0] if rest.strip() else ""

    size = size.split()[0] if size else ""
    return article, size


def format_date(dt: datetime | None) -> str:
    if dt is None:
        return "никогда"
    return dt.strftime("%d.%m.%Y %H:%M")


def days_ago(dt: datetime | None) -> str:
    if dt is None:
        return "никогда"
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    now = datetime.now(timezone.utc)
    delta = now - dt
    days = delta.days
    if days == 0:
        return "сегодня"
    if days == 1:
        return "вчера"
    return f"{days} дней назад"


def status_label(status: str) -> str:
    labels = {
        "new": "🆕 Новый",
        "готов": "✅ Готов",
        "неполный": "🔄 Неполный",
        "архив": "📦 Архив",
    }
    return labels.get(status, status)
