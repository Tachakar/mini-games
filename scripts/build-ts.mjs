import * as esbuild from 'esbuild'
import path from 'path'
import fs from 'fs'

const projectRoot = process.cwd()
const tsSrcDir = path.join(projectRoot, 'ts_src')

const apps = fs.readdirSync(tsSrcDir).filter(app => {
	const appPath = path.join(tsSrcDir, app)
	return fs.statSync(appPath).isDirectory()
})
console.log(`Found apps ${apps.join(', ')}`)

apps.forEach(app => {
	const outDir = path.join(projectRoot, app, 'static', app, 'js')
	if (!fs.existsSync(outDir)) {
		fs.mkdirSync(outDir, { recursive: true })
	}

	esbuild.build({
		entryPoints: [`${tsSrcDir}/${app}/**/*.ts`],
		outdir: outDir,
		bundle: false,
		platform: 'browser',
		format: 'esm',
		target: 'es6',
		loader: { '.ts': 'ts' },
	}).then(() => {
		console.log(`Built ${app} to ${outDir}`)
	}).catch(() => process.exit(1))
})
