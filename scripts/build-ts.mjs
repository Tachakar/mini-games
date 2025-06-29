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
async function buildApps() {
	for (const app of apps) {
		const outDir = path.join(projectRoot, app, 'static', app, 'js')
		try {
			if (!fs.existsSync(outDir)) {
				fs.mkdirSync(outDir, { recursive: true })
			}
			console.log(`Building ${app}`)
			await esbuild.build({
				entryPoints: [`${tsSrcDir}/${app}/*.ts`],
				outdir: outDir,
				bundle: false,
				platform: 'browser',
				format: 'esm',
				target: 'es6',
				loader: { '.ts': 'ts' },
			})
			console.log(`Built ${app} into ${outDir}`)
		} catch (err) {
			console.log(`Failed to build ${app} into ${outDir}`)
			console.log(err)
			process.exit(1)
		}
	}
}
buildApps()
