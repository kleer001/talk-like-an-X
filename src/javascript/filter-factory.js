/**
 * Filter Factory (JavaScript Port)
 * =================================
 *
 * Builds text filters from JSON configuration files.
 *
 * License: GPL
 */

class FilterFactory {
    /**
     * Build a filter from configuration object.
     */
    static fromConfig(config) {
        if (config.type === 'python') {
            return FilterFactory.buildPythonFilter(config);
        }

        return FilterFactory.buildJsonFilter(config);
    }

    /**
     * Build filter from Python module reference.
     */
    static buildPythonFilter(config) {
        const filter = new TextFilter();
        const module = config.module;
        const params = config.params || {};

        let transformer;

        switch (module) {
            case 'duck':
                transformer = new DuckTransformer();
                break;
            case 'studly':
                transformer = new StudlyTransformer(params.seed || 42);
                break;
            case 'lolcat':
                transformer = new LolcatTransformer(params.seed || 42);
                break;
            case 'glitch':
                transformer = new GlitchTransformer(
                    params.percentage || 100,
                    params.seed || 42
                );
                break;
            default:
                throw new Error(`Unknown Python module: ${module}`);
        }

        filter.add(transformer);
        return filter;
    }

    /**
     * Build filter from JSON configuration.
     */
    static buildJsonFilter(config) {
        const filter = new TextFilter();

        if (config.substitutions) {
            filter.add(new Substitution(config.substitutions, {
                wordBoundary: config.word_boundary !== false,
                preserveCase: config.preserve_case !== false
            }));
        }

        if (config.characters) {
            filter.add(new CharacterSubstitution(config.characters, {
                preserveCase: config.preserve_case !== false
            }));
        }

        if (config.suffixes) {
            const suffixReplacer = new SuffixReplacer();
            for (const [suffix, replacement] of Object.entries(config.suffixes)) {
                if (typeof replacement === 'object') {
                    suffixReplacer.addRule(
                        suffix,
                        replacement.replacement,
                        replacement.min_stem || 2
                    );
                } else {
                    suffixReplacer.addRule(suffix, replacement);
                }
            }
            filter.add(suffixReplacer);
        }

        if (config.prefixes) {
            const prefixReplacer = new PrefixReplacer();
            for (const [prefix, replacement] of Object.entries(config.prefixes)) {
                prefixReplacer.addRule(prefix, replacement);
            }
            filter.add(prefixReplacer);
        }

        if (config.sentence_augmentation) {
            const augmenter = new SentenceAugmenter();
            for (const rule of config.sentence_augmentation) {
                augmenter.addRule(
                    rule.punctuation,
                    rule.additions,
                    rule.frequency || 1
                );
            }
            filter.add(augmenter);
        }

        if (config.glitch) {
            const glitchConfig = config.glitch;
            let percentage, seed;

            if (typeof glitchConfig === 'object') {
                percentage = glitchConfig.percentage || 100;
                seed = glitchConfig.seed || 42;
            } else {
                percentage = parseInt(glitchConfig);
                seed = 42;
            }

            filter.add(new GlitchTransformer(percentage, seed));
        }

        if (config.prefix_text) {
            filter.setPrefix(config.prefix_text);
        }

        if (config.suffix_text) {
            filter.setSuffix(config.suffix_text);
        }

        return filter;
    }

    /**
     * Load filter from JSON file URL.
     */
    static async fromJsonFile(url) {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`Failed to load filter: ${url}`);
        }
        const config = await response.json();
        return FilterFactory.fromConfig(config);
    }
}
