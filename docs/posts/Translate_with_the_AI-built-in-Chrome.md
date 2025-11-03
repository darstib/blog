---
date: 2025-08-16
tags:
- blog
comments: true
slug: translate_with_the_ai_built_in_chrome
---

# 使用 Chrome 内置 AI 进行翻译

Chrome 在 138 版本正式开放了三项内置 AI 的 apis（最新情况可见 [api status](https://developer.chrome.com/docs/ai/built-in-apis#api_status)）：

- [Translator API](https://developer.chrome.com/docs/ai/built-in-apis#translator_api)
- [Language Detector API](https://developer.chrome.com/docs/ai/built-in-apis#language_detector_api)
- [Summarizer API](https://developer.chrome.com/docs/ai/built-in-apis#summarizer_api)

显然主要为翻译服务和总结服务；又恰好看见 [fancy-translator](https://github.com/daidr/fancy-translator)，纯前端项目，翻译都在本地且质量不错，但是又有点不爽的地方，故修改后结合 github page 部署一个。

<!-- more -->

## 原版部署

1. 代码获取：要么 fork；要么自己新建一个空仓库，git clone 然后再把 remote_url 设置为你自己的。

	```sh
	$ git clone https://github.com/daidr/fancy-translator.git
	$ git remote set-url origin git@github.com:darstib/fancy-translator.git
	```

2. 添加 `.github/workflows/deploy.yml`

> [!attention]+ CNAME 设置
> 
> 出于方便将 CNAME 直接写在 deploy.yml 中，如果不需要则注释。

> [!info]+ deploy.yml  
> 
> ```yml title="deploy.yml"
> name: Deploy translator to GitHub Pages
>
> on: # 触发器，当项目内容更新时重新部署
>  push:
>    branches: [ main ]
>  pull_request:
>    branches: [ main ]
>
># GITHUB_TOKEN 权限
>permissions:
>  contents: read
>  pages: write
>  id-token: write
>
>concurrency:
>  group: "pages"
>  cancel-in-progress: false
>
>jobs:
>  build:
>    runs-on: ubuntu-latest
>    
>    steps:
>      - name: Checkout
>        uses: actions/checkout@v4
>        
>      - name: Setup Bun
>        uses: oven-sh/setup-bun@v2
>        with:
>          bun-version: latest
>          
>      - name: Cache dependencies
>        uses: actions/cache@v4
>        with:
>          path: ~/.bun/install/cache
>          key: ${{ runner.os }}-bun-${{ hashFiles('**/bun.lock') }}
>          restore-keys: |
>            ${{ runner.os }}-bun-
>            
>      - name: Install dependencies
>        run: bun install --frozen-lockfile
>        
>      - name: Type check
>        run: bun run type-check
>        
>      - name: Lint
>        run: bun run lint
>        
>      - name: Build
>        run: bun run build
>        
>      - name: Setup Pages
>        uses: actions/configure-pages@v5
>        
>      - name: Create CNAME file
>        run: echo "translator.darstib.cn" > dist/CNAME
>        
>      - name: Upload artifact
>        uses: actions/upload-pages-artifact@v3
>        with:
>          path: ./dist
>
>  deploy:
>    environment:
>      name: github-pages
>      url: ${{ steps.deployment.outputs.page_url }}
>    runs-on: ubuntu-latest
>    needs: build
>    if: github.ref == 'refs/heads/main'
>    
>    steps:
>      - name: Deploy to GitHub Pages
>        id: deployment
>        uses: actions/deploy-pages@v4
> ```

3. 更新仓库后还应该在 https://github.com/you-username/fancy-translator/settings/pages 中开启 github page。

![fancy-translator|600](https://raw.githubusercontent.com/darstib/public_imgs/PicGo//PicGo_exe/fancy-translator.png)


## 一点点改进

实际上手发现默认行为为：自动检测语言，下载对应的翻译模型，并翻译为中文，基于：

```ts title="src/stores/translator.ts"
function updateLangPair(params: { sourceLanguage: string, targetLanguage: string }) {
  let { sourceLanguage, targetLanguage } = params
  if (!sourceLanguage || !targetLanguage) {
    // 若存在空参数，首先进行空参数补全
    if (!sourceLanguage) {
      // 默认源语言为中文
      sourceLanguage = isLanguageDetectorSupported ? 'auto' : 'zh-Hans'
    }
    if (!targetLanguage) {
      const defaultTargetLanguage = 'en'
      targetLanguage = defaultTargetLanguage
    }
  }
  _sourceLanguage.value = sourceLanguage
  _targetLanguage.value = targetLanguage

  // 若源语言为自动检测，但是不支持语言检测，默认源语言为中文
  if (_sourceLanguage.value === 'auto' && !isLanguageDetectorSupported) {
    _sourceLanguage.value = 'zh-Hans'
  }

  // 若源语言为自动检测，则初始化LanguageDetector
  if (_sourceLanguage.value === 'auto') {
    initLanguageDetector()
  }

  translate(_sourceText.value)
}
```

但是这时候一个比较尴尬的情况是如果我希望中文翻译为英文，将会出现“不支持 zh 到 zh-Hans 的翻译”。固然可以将目标语言手动设置为英文，但是显然我加入一个小 trick 能让我自己用的更舒服：

```ts title="src/stores/translator.ts" hl_lines="40-43"
  async function translate(text: string) {
    // ...
	if (sourceLanguage === 'auto') {
	  // 此时需要使用语言检测模型
	  if (!languageDetectorStatus.value?.instance) {
	    await initLanguageDetector()
	  }
	  if (isOutdated()) {
	    return
	  }
	  if (!languageDetectorStatus.value?.instance) {
	    isTranslating.value = false
	    return
	  }
	  languageDetectionList.value = []
	  const detectedLanguage = await languageDetectorStatus.value.instance.detect(text, {
	    signal: controller.signal,
	  }).catch(() => {
	    return []
	  })
	  if (isOutdated()) {
	    return
	  }
	  languageDetectionList.value = detectedLanguage
	  sourceLanguage = detectedLanguage[0].detectedLanguage
	  if (sourceLanguage === 'und') {
	    // 未知语言
	    sourceLanguage = 'und'
	    translateResult.value = {
	      error: new Error(t('language_detection_failed')),
	      result: '',
	    }
	  }
	  _realSourceLanguage.value = sourceLanguage
	}
	else {
	  _realSourceLanguage.value = sourceLanguage
	}
	
	// 若源语言和目标语言均为中文，则默认翻译为英文
	if (_realSourceLanguage.value === 'zh' && _targetLanguage.value === 'zh-Hans') {
	  _targetLanguage.value = 'en'
	}
	//...
```

逻辑也很简单，有需要也可以自己加/改。