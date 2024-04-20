from fuzzywuzzy import fuzz

keywords_en = ["expo", "khan-shatyr", "mega-silk-way", "baiterek"]
keywords_ru = ["Экспо", "Хан Шатыр", "МегаСилкВей", "Байтерек"]


def find_most_similar_keyword(user_input):
    max_similarity_en = 0
    most_similar_keyword_en = None

    max_similarity_ru = 0
    most_similar_keyword_ru = None

    for keyword in keywords_en:
        similarity_score = fuzz.ratio(user_input.lower(), keyword.lower())
        if similarity_score > max_similarity_en:
            max_similarity_en = similarity_score
            most_similar_keyword_en = keyword

    for keyword in keywords_ru:
        similarity_score = fuzz.ratio(user_input.lower(), keyword.lower())
        if similarity_score > max_similarity_ru:
            max_similarity_ru = similarity_score
            most_similar_keyword_ru = keyword

    if max_similarity_en > max_similarity_ru:
        if max_similarity_en >= 55:
            return most_similar_keyword_en
        else:
            return None
    else:
        if max_similarity_ru >= 55:
            return most_similar_keyword_ru
        else:
            return None


def process_user_input(user_input):
    most_similar_keyword = find_most_similar_keyword(user_input)
    if most_similar_keyword is not None:
        if most_similar_keyword in keywords_en:
            return "English", most_similar_keyword
        elif most_similar_keyword in keywords_ru:
            idx_ru = keywords_ru.index(most_similar_keyword)
            most_similar_keyword_en = keywords_en[idx_ru]
            return "Russian", most_similar_keyword_en
    else:
        return "Not Found", None