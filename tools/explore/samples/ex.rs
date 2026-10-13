// Compte les mots d'un texte
use std::collections::HashMap;

pub struct Counter {
    words: HashMap<String, usize>,
}

impl Counter {
    pub fn add(&mut self, text: &str) -> usize {
        for w in text.split_whitespace() {
            *self.words.entry(w.to_lowercase()).or_insert(0) += 1;
        }
        self.words.len()
    }
}
