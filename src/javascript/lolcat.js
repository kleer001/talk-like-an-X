/**
 * LOLCAT Filter
 * ==============
 *
 * Converts text to LOLCAT speak with random capitalization and common substitutions.
 *
 * License: GPL-2+
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
