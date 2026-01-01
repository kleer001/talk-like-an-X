/**
 * Studly Caps Filter
 * ===================
 *
 * Randomly capitalizes letters to create "StUdLy CaPs" effect.
 *
 * Author: Nick Phillips (original)
 * License: GPL-2+
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
