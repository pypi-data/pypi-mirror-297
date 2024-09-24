def thyroAI(image_urls, language="English", base_url="http://20.240.210.52:1688/v1/",
            api_key="sk-Qjeu6nlITz74zmsP92Cf6c53C89b44B3A0232c0f15564021"):
    import pandas as pd
    from openai import OpenAI
    prompt_Chinese=f"""
        As a pathology expert, analyze a single uploaded thyroid FNA biopsy image for educational and research purposes. When an image is uploaded, the GPT will start its response by exactly repeating the image number from the label (e.g., "20200120085309323_h.jpg") on a new line before beginning the analysis. It provides responses in two distinct parts: a detailed analysis comparing observed features to typical pathological features, then a strict, direct scoring of the following sixteen cytological characteristics, formatted for easy extraction into spreadsheets, with scores ranging from 0 (absent) to 10 (very prominent):
        1. Cells arranged in papillae and/or monolayers: [score] ([description])
        2. Cellular swirls ("onion-skin" or “cartwheel" patterns) in some cases: [score] ([description])
        3. Enlarged and crowded nuclei, often molded: [score] ([description])
        4. Oval or irregularly shaped nuclei: [score] ([description])
        5. Longitudinal nuclear grooves: [score] ([description])
        6. Intranuclear cytoplasmic pseudoinclusions (INCls): [score] ([description])
        7. Pale nuclei with powdery chromatin: [score] ([description])
        8. Thick nuclear membranes: [score] ([description])
        9. Marginally placed micronucleoli, solitary or multiple: [score] ([description])
        10. Psammoma bodies: [score] ([description])
        11. Multinucleated giant cells: [score] ([description])
        12. Variable amount of colloid; may be stringy, ropy, or “bubblegum”-like: [score] ([description])
        13. “Hobnail” cells: [score] ([description])
        14. Oncocytic (Hürthle cell) metaplasia: [score] ([description])
        15. Squamoid metaplasia: [score] ([description])
        16. “Histiocytoid” cells: [score] ([description])
        The conclusion is formatted as '结论: [恶性/良性/不确定] ([description]),' based on the overall evaluation of key features and malignancy degree, providing a clear and concise conclusion. On a new line after the conclusion: '恶性程度: [0-10分]', reflecting the malignancy degree in a format suitable for spreadsheet extraction. All responses are delivered in Chinese.
        """

    prompt_English=f"""
        As a pathology expert, analyze a single uploaded thyroid FNA biopsy image for educational and research purposes. When an image is uploaded, the GPT will start its response by exactly repeating the image number from the label (e.g., "20200120085309323_h.jpg") on a new line before beginning the analysis. It provides responses in two distinct parts: a detailed analysis comparing observed features to typical pathological features, then a strict, direct scoring of the following sixteen cytological characteristics, formatted for easy extraction into spreadsheets, with scores ranging from 0 (absent) to 10 (very prominent):
        1. Cells arranged in papillae and/or monolayers: [score] ([description])
        2. Cellular swirls ("onion-skin" or “cartwheel" patterns) in some cases: [score] ([description])
        3. Enlarged and crowded nuclei, often molded: [score] ([description])
        4. Oval or irregularly shaped nuclei: [score] ([description])
        5. Longitudinal nuclear grooves: [score] ([description])
        6. Intranuclear cytoplasmic pseudoinclusions (INCls): [score] ([description])
        7. Pale nuclei with powdery chromatin: [score] ([description])
        8. Thick nuclear membranes: [score] ([description])
        9. Marginally placed micronucleoli, solitary or multiple: [score] ([description])
        10. Psammoma bodies: [score] ([description])
        11. Multinucleated giant cells: [score] ([description])
        12. Variable amount of colloid; may be stringy, ropy, or “bubblegum”-like: [score] ([description])
        13. “Hobnail” cells: [score] ([description])
        14. Oncocytic (Hürthle cell) metaplasia: [score] ([description])
        15. Squamoid metaplasia: [score] ([description])
        16. “Histiocytoid” cells: [score] ([description])
        The conclusion is formatted as 'Conclusion: [Malignant/Benign/Uncertain] ([description]),' based on the overall evaluation of key features and malignancy degree, providing a clear and concise conclusion. On a new line after the conclusion: '恶性程度: [0-10分]', reflecting the malignancy degree in a format suitable for spreadsheet extraction. All responses are delivered in English.
        """
    
    # 设置API key
    client = OpenAI(base_url=base_url, api_key=api_key)

    # 根据语言选择不同的 prompt
    if language == "English":
        prompt =   prompt_English# 替换为实际的英文 prompt
    elif language == "Chinese":
        prompt =   prompt_Chinese  # 替换为实际的中文 prompt
    else:
        raise ValueError("Unsupported language. Please choose 'English' or 'Chinese'.")

    # 调用 GPT 模型
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": image_urls}}
                ]
            }
        ],
        model="gpt-4o",  # 可以切换为 "gpt-3.5-turbo" 模型
        temperature=0.4  # 控制生成文本的随机性
    )

    # 输出生成的结果
    return(print(chat_completion.choices[0].message.content))
