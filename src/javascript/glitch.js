/**
 * Glitch Filter
 * ==============
 *
 * Corrupts text by replacing characters with Unicode blocks and shapes.
 *
 * License: GPL
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
