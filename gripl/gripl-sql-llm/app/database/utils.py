def get_db_schema_string():
    return """
        gdpr_articles(
    id INTEGER PRIMARY KEY,
    article_number VARCHAR(2) NOT NULL,
    paragraph VARCHAR(2),
    literature VARCHAR(2),
    text TEXT NOT NULL
)

category(
    id INTEGER PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL
)

gdpr_criteria(
    id INTEGER PRIMARY KEY,
    category_id INTEGER NOT NULL,
    short_name VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    FOREIGN KEY (category_id) REFERENCES category(id)
)

criterion_article_association(
    criterion_id INTEGER NOT NULL,
    article_id INTEGER NOT NULL,
    PRIMARY KEY (criterion_id, article_id),
    FOREIGN KEY (criterion_id) REFERENCES gdpr_criteria(id),
    FOREIGN KEY (article_id) REFERENCES gdpr_articles(id)
)
    """