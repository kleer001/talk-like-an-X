#!/usr/bin/env python3
"""
Talk Like An X - Web Demo
==========================

Flask web application providing an interactive demo of the text transformation filters.

Author: Talk Like An X Project
License: GPL
"""

import sys
from pathlib import Path
from typing import Dict, List
from flask import Flask, render_template, request, jsonify

sys.path.insert(0, str(Path(__file__).parent.parent / 'src' / 'python'))

from filter_factory import FilterFactory


class WebDemo:
    """Web demo application for Talk Like An X filters."""

    def __init__(self, filters_directory: Path):
        """
        Initialize the web demo with available filters.

        Args:
            filters_directory: Path to directory containing filter JSON files
        """
        self.filters_directory = filters_directory
        self.available_filters = self._discover_filters()

    def _discover_filters(self) -> List[Dict[str, str]]:
        """
        Discover all available filter JSON files.

        Returns:
            List of dicts with 'id' and 'name' for each filter
        """
        filters = []
        for json_file in sorted(self.filters_directory.glob('*.json')):
            filter_id = json_file.stem
            filter_name = self._format_filter_name(filter_id)
            filters.append({'id': filter_id, 'name': filter_name})
        return filters

    @staticmethod
    def _format_filter_name(filter_id: str) -> str:
        """
        Convert filter ID to human-readable name.

        Args:
            filter_id: Filter identifier (e.g., 'disco' or 'beatnik_1950s')

        Returns:
            Formatted name (e.g., 'Disco' or 'Beatnik (1950s)')
        """
        parts = filter_id.replace('_', ' ').split()

        formatted_parts = []
        for part in parts:
            if part.isdigit() or (part.endswith('s') and part[:-1].isdigit()):
                formatted_parts.append(f'({part})')
            else:
                formatted_parts.append(part.capitalize())

        return ' '.join(formatted_parts)

    def transform_text(self, filter_id: str, text: str) -> str:
        """
        Apply a filter transformation to input text.

        Args:
            filter_id: ID of the filter to apply
            text: Input text to transform

        Returns:
            Transformed text

        Raises:
            FileNotFoundError: If filter does not exist
            ValueError: If filter configuration is invalid
        """
        filter_path = self.filters_directory / f'{filter_id}.json'
        if not filter_path.exists():
            raise FileNotFoundError(f'Filter {filter_id} not found')

        text_filter = FilterFactory.from_json(str(filter_path))
        return text_filter.transform(text)


app = Flask(__name__)
demo = WebDemo(Path(__file__).parent.parent / 'src' / 'filters')


@app.route('/')
def index():
    """Render the main demo page."""
    return render_template('index.html', filters=demo.available_filters)


@app.route('/transform', methods=['POST'])
def transform():
    """
    API endpoint for text transformation.

    Expected JSON payload:
        {
            "filter": "disco",
            "text": "Hello world"
        }

    Returns:
        JSON response with transformed text or error
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({'error': 'No data provided'}), 400

        filter_id = data.get('filter')
        text = data.get('text', '')

        if not filter_id:
            return jsonify({'error': 'Filter not specified'}), 400

        if not text:
            return jsonify({'error': 'No text provided'}), 400

        transformed = demo.transform_text(filter_id, text)
        return jsonify({'result': transformed})

    except FileNotFoundError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': f'Transformation failed: {str(e)}'}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
