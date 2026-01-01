/**
 * Duck Filter
 * ===========
 *
 * Replaces all words with variations of "quack" based on word length.
 *
 * Author: Aaron Wells (2023)
 * License: Public domain
 */

class DuckTransformer {
    transform(text) {
        function sameCap(original, replacement) {
            if (!original) return replacement;

            if (original === original.toUpperCase()) {
                return replacement.toUpperCase();
            } else if (original[0] === original[0].toUpperCase()) {
                return replacement[0].toUpperCase() + replacement.slice(1);
            } else {
                return replacement.toLowerCase();
            }
        }

        function duckWord(match) {
            const word = match;
            const length = word.length;

            let duck;
            if (length <= 3) {
                duck = 'qua';
            } else if (length >= 10) {
                duck = 'quackquack';
            } else {
                duck = 'quack';
            }

            return sameCap(word, duck);
        }

        return text.replace(/[a-zA-Z]+/g, duckWord);
    }
}
