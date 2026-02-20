#!/usr/bin/env python3
import os
import sys
from flask import Flask, render_template, jsonify, request, send_from_directory
import argparse

app = Flask(__name__)
app.config['INPUT_DIR'] = ''
app.config['OUTPUT_DIR'] = ''

def get_image_pairs():
    input_dir = app.config['INPUT_DIR']
    output_dir = app.config['OUTPUT_DIR']
    
    if not input_dir or not output_dir:
        return []
    
    image_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp'}
    pairs = []
    
    for filename in os.listdir(input_dir):
        ext = os.path.splitext(filename)[1].lower()
        if ext in image_extensions:
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename)
            if os.path.exists(output_path):
                txt_filename = os.path.splitext(filename)[0] + '.txt'
                txt_path = os.path.join(output_dir, txt_filename)
                flag_filename = os.path.splitext(filename)[0] + '.flag'
                flag_path = os.path.join(output_dir, flag_filename)
                
                txt_content = ''
                if os.path.exists(txt_path):
                    try:
                        with open(txt_path, 'r') as f:
                            txt_content = f.read().strip()
                    except Exception:
                        txt_content = ''
                
                pairs.append({
                    'filename': filename,
                    'input': f'/input/{filename}',
                    'output': f'/output/{filename}',
                    'input_full_path': input_path,
                    'output_full_path': output_path,
                    'has_txt': os.path.exists(txt_path),
                    'has_flag': os.path.exists(flag_path),
                    'txt_content': txt_content
                })
    
    return sorted(pairs, key=lambda x: x['filename'])

@app.route('/')
def index():
    pairs = get_image_pairs()
    return render_template('index.html', pairs=pairs)

@app.route('/input/<path:filename>')
def serve_input(filename):
    print(app.config['INPUT_DIR'], filename)
    return send_from_directory(app.config['INPUT_DIR'], filename)

@app.route('/output/<path:filename>')
def serve_output(filename):
    return send_from_directory(app.config['OUTPUT_DIR'], filename)

@app.route('/api/pairs')
def api_pairs():
    return jsonify(get_image_pairs())

@app.route('/api/confirm', methods=['POST'])
def confirm():
    data = request.json
    filename = data.get('filename')
    color = data.get('color')
    custom_prompt = data.get('custom_prompt', '').strip()
    
    output_dir = app.config['OUTPUT_DIR']
    txt_filename = os.path.splitext(filename)[0] + '.txt'
    txt_path = os.path.join(output_dir, txt_filename)
    
    if custom_prompt:
        content = custom_prompt
    else:
        content = f"Create a black and white alpha mask of the object outlined in {color}"
    
    with open(txt_path, 'w') as f:
        f.write(content)
    
    flag_filename = os.path.splitext(filename)[0] + '.flag'
    flag_path = os.path.join(output_dir, flag_filename)
    if os.path.exists(flag_path):
        os.remove(flag_path)
    
    return jsonify({'success': True, 'path': txt_path})

@app.route('/api/flag', methods=['POST'])
def flag():
    data = request.json
    filename = data.get('filename')
    
    output_dir = app.config['OUTPUT_DIR']
    flag_filename = os.path.splitext(filename)[0] + '.flag'
    flag_path = os.path.join(output_dir, flag_filename)
    
    with open(flag_path, 'w') as f:
        f.write('needs manual edit')
    
    return jsonify({'success': True, 'path': flag_path})

@app.route('/api/delete', methods=['POST'])
def delete():
    data = request.json
    filename = data.get('filename')
    
    input_dir = app.config['INPUT_DIR']
    output_dir = app.config['OUTPUT_DIR']
    
    input_path = os.path.join(input_dir, filename)
    output_path = os.path.join(output_dir, filename)
    flag_path = os.path.join(output_dir, os.path.splitext(filename)[0] + '.flag')
    txt_path = os.path.join(output_dir, os.path.splitext(filename)[0] + '.txt')
    
    deleted = []
    if os.path.exists(input_path):
        os.remove(input_path)
        deleted.append(input_path)
    if os.path.exists(output_path):
        os.remove(output_path)
        deleted.append(output_path)
    if os.path.exists(flag_path):
        os.remove(flag_path)
        deleted.append(flag_path)
    if os.path.exists(txt_path):
        os.remove(txt_path)
        deleted.append(txt_path)
    
    return jsonify({'success': True, 'deleted': deleted})

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Image pair examiner')
    parser.add_argument('input_dir', help='Directory containing input images')
    parser.add_argument('output_dir', help='Directory containing mask output images')
    parser.add_argument('--port', type=int, default=5000, help='Port to run on')
    
    args = parser.parse_args()
    
    if not os.path.isdir(args.input_dir):
        print(f"Error: Input directory '{args.input_dir}' does not exist")
        sys.exit(1)
    
    if not os.path.isdir(args.output_dir):
        print(f"Error: Output directory '{args.output_dir}' does not exist")
        sys.exit(1)
    
    app.config['INPUT_DIR'] = os.path.abspath(args.input_dir)
    app.config['OUTPUT_DIR'] = os.path.abspath(args.output_dir)
    
    print(f"Input directory: {app.config['INPUT_DIR']}")
    print(f"Output directory: {app.config['OUTPUT_DIR']}")
    print(f"Running on http://localhost:{args.port}")
    
    app.run(debug=True, port=args.port)
