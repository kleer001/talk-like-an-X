/**
 * Text Transformation Library (JavaScript Port)
 * ==============================================
 *
 * Generalized library for creating text filters.
 * Ported from Python implementation.
 *
 * License: GPL
 */

/**
 * Preserve capitalization pattern from original text.
 */
function sameCap(original, replacement) {
    if (!original || !replacement) return replacement;

    if (original === original.toUpperCase()) {
        return replacement.toUpperCase();
    } else if (original[0] === original[0].toUpperCase()) {
        return replacement[0].toUpperCase() + replacement.slice(1);
    } else {
        return replacement[0].toLowerCase() + replacement.slice(1);
    }
}

/**
 * Base class for regex-based transformers.
 */
class RegexTransformer {
    constructor() {
        this.rules = [];
    }

    addRule(pattern, replacer, flags = '') {
        this.rules.push({
            pattern: new RegExp(pattern, flags),
            replacer
        });
    }

    transform(text) {
        let result = text;
        for (const { pattern, replacer } of this.rules) {
            result = result.replace(pattern, replacer);
        }
        return result;
    }
}

/**
 * Word and phrase substitution transformer.
 */
class Substitution extends RegexTransformer {
    constructor(mappings, options = {}) {
        super();
        const wordBoundary = options.wordBoundary !== false;
        const preserveCase = options.preserveCase !== false;

        this.compileMappings(mappings, wordBoundary, preserveCase);
    }

    compileMappings(mappings, wordBoundary, preserveCase) {
        const sortedEntries = Object.entries(mappings)
            .sort((a, b) => b[0].length - a[0].length);

        for (const [original, replacement] of sortedEntries) {
            let pattern;

            if (original.includes(' ')) {
                const words = original.split(' ').map(w =>
                    w.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
                );
                pattern = words.join('\\s+');
            } else {
                pattern = original.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
            }

            if (wordBoundary) {
                pattern = '\\b' + pattern + '\\b';
            }

            const flags = preserveCase ? 'gi' : 'g';
            const replacer = preserveCase
                ? (match) => sameCap(match, replacement)
                : () => replacement;

            this.addRule(pattern, replacer, flags);
        }
    }
}

/**
 * Character substitution transformer.
 */
class CharacterSubstitution extends RegexTransformer {
    constructor(mappings, options = {}) {
        super();
        const preserveCase = options.preserveCase !== false;

        const sortedEntries = Object.entries(mappings)
            .sort((a, b) => b[0].length - a[0].length);

        for (const [original, replacement] of sortedEntries) {
            const pattern = original.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
            const flags = preserveCase ? 'gi' : 'g';
            const replacer = preserveCase
                ? (match) => sameCap(match, replacement)
                : () => replacement;

            this.addRule(pattern, replacer, flags);
        }
    }
}

/**
 * Suffix replacement transformer.
 */
class SuffixReplacer extends RegexTransformer {
    addRule(suffix, replacement, minStem = 2) {
        const pattern = `([a-zA-Z]{${minStem},})${suffix.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}\\b`;
        const replacer = (match, stem) => stem + replacement;
        super.addRule(pattern, replacer, 'gi');
    }
}

/**
 * Prefix replacement transformer.
 */
class PrefixReplacer extends RegexTransformer {
    addRule(prefix, replacement) {
        const pattern = `\\b${prefix.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}([a-zA-Z]+)`;
        const replacer = (match, rest) => replacement + rest;
        super.addRule(pattern, replacer, 'gi');
    }
}

/**
 * Sentence augmentation transformer.
 */
class SentenceAugmenter {
    constructor() {
        this.rules = [];
        this.counters = {};
    }

    addRule(punctuation, additions, frequency = 1) {
        this.rules.push({ punctuation, additions, frequency });
        if (frequency > 1) {
            this.counters[punctuation] = 0;
        }
    }

    transform(text) {
        let result = text;

        for (const { punctuation, additions, frequency } of this.rules) {
            const parts = result.split(punctuation);
            const newParts = [];

            if (frequency === 1) {
                for (let i = 0; i < parts.length - 1; i++) {
                    newParts.push(parts[i] + punctuation + additions[i % additions.length]);
                }
                newParts.push(parts[parts.length - 1]);
            } else {
                let counter = this.counters[punctuation] || 0;

                for (let i = 0; i < parts.length - 1; i++) {
                    newParts.push(parts[i] + punctuation);
                    if (counter % frequency === 0) {
                        newParts.push(additions[counter % additions.length]);
                    }
                    counter++;
                }
                newParts.push(parts[parts.length - 1]);
                this.counters[punctuation] = counter;
            }

            result = newParts.join('');
        }

        return result;
    }
}

/**
 * Glitch transformer (corruption effect).
 */
class GlitchTransformer {
    static GLITCH_CHARS = [
        '█', '▓', '▒', '░', '▀', '▄', '▌', '▐', '■', '□',
        '▪', '▫', '▬', '▭', '▮', '▯', '▰', '▱', '▲', '△',
        '▴', '▵', '▶', '▷', '▸', '▹', '►', '▻', '▼', '▽',
        '▾', '▿', '◀', '◁', '◂', '◃', '◄', '◅', '◆', '◇',
        '◈', '◉', '◊', '○', '◌', '◍', '◎', '●', '◐', '◑',
        '◒', '◓', '◔', '◕', '◖', '◗', '◘', '◙', '◚', '◛',
    ];

    constructor(percentage = 100, seed = 42) {
        this.percentage = percentage;
        this.random = new SeededRandom(seed);
    }

    transform(text) {
        const result = [];

        for (const char of text) {
            if (/[a-zA-Z0-9]/.test(char) && this.random.randInt(1, 100) <= this.percentage) {
                result.push(this.random.choice(GlitchTransformer.GLITCH_CHARS));
            } else {
                result.push(char);
            }
        }

        return result.join('');
    }
}

/**
 * Seeded random number generator for reproducible results.
 */
class SeededRandom {
    constructor(seed) {
        this.seed = seed;
        this.m = 0x80000000;
        this.a = 1103515245;
        this.c = 12345;
        this.state = seed ? seed : Math.floor(Math.random() * (this.m - 1));
    }

    randInt(min, max) {
        this.state = (this.a * this.state + this.c) % this.m;
        return min + Math.floor((this.state / this.m) * (max - min + 1));
    }

    random() {
        this.state = (this.a * this.state + this.c) % this.m;
        return this.state / this.m;
    }

    choice(array) {
        return array[this.randInt(0, array.length - 1)];
    }
}

/**
 * Main text filter engine.
 */
class TextFilter {
    constructor() {
        this.transformers = [];
        this.prefix = '';
        this.suffix = '';
    }

    add(transformer) {
        this.transformers.push(transformer);
    }

    setPrefix(prefix) {
        this.prefix = prefix;
    }

    setSuffix(suffix) {
        this.suffix = suffix;
    }

    transform(text) {
        let result = text;
        for (const transformer of this.transformers) {
            result = transformer.transform(result);
        }
        return this.prefix + result + this.suffix;
    }
}
