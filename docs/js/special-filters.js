/**
 * Special Algorithmic Filters (JavaScript Port)
 * ==============================================
 *
 * Ports of duck, glitch, studly, and lolcat filters.
 *
 * License: GPL
 */

/**
 * Duck filter transformer.
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
            const word = match[0];
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

/**
 * Studly caps transformer.
 */
class StudlyTransformer {
    constructor(seed = 42) {
        this.random = new SeededRandom(seed);
    }

    transform(text) {
        const result = [];

        for (const char of text) {
            if (/[a-zA-Z]/.test(char)) {
                if (this.random.random() < 0.5) {
                    result.push(char.toUpperCase());
                } else {
                    result.push(char.toLowerCase());
                }
            } else {
                result.push(char);
            }
        }

        return result.join('');
    }
}

/**
 * LOLCAT transformer.
 */
class LolcatTransformer {
    constructor(seed = 42) {
        this.random = new SeededRandom(seed);
        this.substitutions = {
            'you': 'u',
            'your': 'ur',
            "you're": 'ur',
            'ok': 'k',
            'okay': 'k',
            'the': 'teh',
            'more': 'moar',
            'my': 'mah',
            'are': 'r',
            'what': 'wut',
            'cute': 'kyoot',
            'please': 'plz',
            'thanks': 'thx',
            'because': 'cuz',
            'love': 'luv',
            'oh': 'o',
            'to': '2',
            'too': '2',
            'for': '4',
        };
    }

    transform(text) {
        let result = text;

        for (const [old, newWord] of Object.entries(this.substitutions)) {
            const pattern = new RegExp(`\\b${old.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}\\b`, 'gi');
            result = result.replace(pattern, newWord);
        }

        const chars = [];
        for (const char of result) {
            if (/[a-zA-Z]/.test(char)) {
                if (this.random.random() < 0.3) {
                    chars.push(char.toUpperCase());
                } else {
                    chars.push(char.toLowerCase());
                }
            } else {
                chars.push(char);
            }
        }

        return chars.join('');
    }
}
