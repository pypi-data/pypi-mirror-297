"use strict";
(self["webpackChunk_jupyter_shared_docprovider_extension"] = self["webpackChunk_jupyter_shared_docprovider_extension"] || []).push([["shared-docprovider_lib_index_js"],{

/***/ "../shared-docprovider/lib/drive.js":
/*!******************************************!*\
  !*** ../shared-docprovider/lib/drive.js ***!
  \******************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   SharedDrive: () => (/* binding */ SharedDrive)
/* harmony export */ });
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var y_webrtc__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! y-webrtc */ "webpack/sharing/consume/default/y-webrtc/y-webrtc");
/* harmony import */ var y_webrtc__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(y_webrtc__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @lumino/signaling */ "webpack/sharing/consume/default/@lumino/signaling");
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_lumino_signaling__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyter_ydoc__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @jupyter/ydoc */ "webpack/sharing/consume/default/@jupyter/ydoc");
/* harmony import */ var _jupyter_ydoc__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyter_ydoc__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @jupyterlab/services */ "webpack/sharing/consume/default/@jupyterlab/services");
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_services__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _provider__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./provider */ "../shared-docprovider/lib/provider.js");
/* harmony import */ var _path__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ./path */ "../shared-docprovider/lib/path.js");
/* harmony import */ var _ydrive__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./ydrive */ "../shared-docprovider/lib/ydrive.js");
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.









const signalingServers = JSON.parse(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_3__.PageConfig.getOption('signalingServers'));
/**
 * A collaborative implementation for an `IDrive`, talking to other peers using WebRTC.
 */
class SharedDrive {
    /**
     * Construct a new drive object.
     *
     * @param user - The user manager to add the identity to the awareness of documents.
     */
    constructor(user, defaultFileBrowser, translator, globalAwareness, name) {
        this._onSync = (synced) => {
            var _a;
            if (synced.synced) {
                this._ready.resolve();
                (_a = this._fileSystemProvider) === null || _a === void 0 ? void 0 : _a.off('synced', this._onSync);
            }
        };
        this._onCreate = (options) => {
            if (typeof options.format !== 'string') {
                const factory = this.sharedModelFactory.documentFactories.get(options.contentType);
                const sharedModel = factory(options);
                return sharedModel;
            }
            // Check if file exists.
            this._ydrive.get(options.path);
            const key = `${options.format}:${options.contentType}:${options.path}`;
            // Check if shared model alread exists.
            const fileProvider = this._fileProviders.get(key);
            if (fileProvider) {
                return fileProvider.sharedModel;
            }
            const factory = this.sharedModelFactory.documentFactories.get(options.contentType);
            const sharedModel = factory(options);
            const provider = new _provider__WEBPACK_IMPORTED_MODULE_6__.WebrtcProvider({
                url: '',
                path: options.path,
                format: options.format,
                contentType: options.contentType,
                model: sharedModel,
                user: this._user,
                translator: this._trans,
                signalingServers: this._signalingServers
            });
            this._fileProviders.set(key, { provider, sharedModel });
            sharedModel.disposed.connect(() => {
                const fileProvider = this._fileProviders.get(key);
                if (fileProvider) {
                    fileProvider.provider.dispose();
                    this._fileProviders.delete(key);
                }
            });
            return sharedModel;
        };
        this._fileChanged = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_2__.Signal(this);
        this._isDisposed = false;
        this._ydrive = new _ydrive__WEBPACK_IMPORTED_MODULE_7__.YDrive();
        this._ready = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__.PromiseDelegate();
        this._signalingServers = [];
        this._user = user;
        this._defaultFileBrowser = defaultFileBrowser;
        this._trans = translator;
        this._globalAwareness = globalAwareness;
        //this._username = this._globalAwareness?.getLocalState()?.user.identity.name;
        //this._username = this._globalAwareness?.getLocalState()?.username;
        this._fileProviders = new Map();
        this.sharedModelFactory = new SharedModelFactory(this._onCreate);
        this.serverSettings = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_5__.ServerConnection.makeSettings();
        signalingServers.forEach((url) => {
            if (url.startsWith('ws://') ||
                url.startsWith('wss://') ||
                url.startsWith('http://') ||
                url.startsWith('https://')) {
                // It's an absolute URL, keep it as-is.
                this._signalingServers.push(url);
            }
            else {
                // It's a Jupyter server relative URL, build the absolute URL.
                this._signalingServers.push(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_3__.URLExt.join(this.serverSettings.wsUrl, url));
            }
        });
        this.name = name;
        this._fileSystemProvider = new y_webrtc__WEBPACK_IMPORTED_MODULE_1__.WebrtcProvider('fileSystem', this._ydrive.ydoc, {
            signaling: this._signalingServers,
            awareness: this._globalAwareness || undefined
        });
        this._fileSystemProvider.on('synced', this._onSync);
    }
    //get providers(): Map<string, WebrtcProvider> {
    get providers() {
        // FIXME
        const providers = new Map();
        for (const key in this._fileProviders) {
            providers.set(key, this._fileProviders.get(key).provider);
        }
        return providers;
    }
    async getDownloadUrl(path) {
        return '';
    }
    async delete(localPath) {
        this._ydrive.delete(localPath);
    }
    async restoreCheckpoint(path, checkpointID) { }
    async deleteCheckpoint(path, checkpointID) { }
    async importFile(path) {
        const model = await this._defaultFileBrowser.model.manager.services.contents.get(path, {
            content: true
        });
        this._ydrive.createFile(model.name); // FIXME: create file in cwd?
        const sharedModel = this.sharedModelFactory.createNew({
            path: model.name,
            format: model.format,
            contentType: model.type,
            collaborative: true
        });
        if (sharedModel) {
            // FIXME: replace with sharedModel.source=model.content
            // when https://github.com/jupyter-server/jupyter_ydoc/pull/273 is merged
            if (sharedModel instanceof _jupyter_ydoc__WEBPACK_IMPORTED_MODULE_4__.YNotebook) {
                sharedModel.fromJSON(model.content);
            }
            else {
                sharedModel.setSource(model.content);
            }
        }
    }
    async newUntitled(options = {}) {
        var _a;
        let ext = '';
        let isDir = false;
        if (options.type === 'directory') {
            isDir = true;
        }
        else if (options.type === 'notebook') {
            ext = '.ipynb';
        }
        else {
            ext = '.txt';
        }
        const newPath = this._ydrive.newUntitled(isDir, options.path, ext);
        const newName = new _path__WEBPACK_IMPORTED_MODULE_8__.Path(newPath).name;
        const model = {
            name: newName,
            path: newPath,
            type: (_a = options.type) !== null && _a !== void 0 ? _a : 'file',
            writable: true,
            created: '',
            last_modified: '',
            mimetype: '',
            content: null,
            format: null
        };
        this._fileChanged.emit({
            type: 'new',
            oldValue: null,
            newValue: model
        });
        return model;
    }
    async rename(path, newPath) {
        this._ydrive.move(path, newPath);
        const model = {
            name: new _path__WEBPACK_IMPORTED_MODULE_8__.Path(newPath).name,
            path: newPath,
            type: 'file',
            writable: true,
            created: '',
            last_modified: '',
            mimetype: '',
            content: null,
            format: null
        };
        return model;
    }
    async copy(path, toDir) {
        throw new Error('Copy/paste not supported');
    }
    async createCheckpoint(path) {
        return {
            id: '',
            last_modified: ''
        };
    }
    async listCheckpoints(path) {
        return [];
    }
    /**
     * A signal emitted when a file operation takes place.
     */
    get fileChanged() {
        return this._fileChanged;
    }
    /**
     * Test whether the manager has been disposed.
     */
    get isDisposed() {
        return this._isDisposed;
    }
    /**
     * Dispose of the resources held by the manager.
     */
    dispose() {
        if (this.isDisposed) {
            return;
        }
        this._fileProviders.forEach(fp => fp.provider.dispose());
        this._fileProviders.clear();
        this._isDisposed = true;
        _lumino_signaling__WEBPACK_IMPORTED_MODULE_2__.Signal.clearData(this);
    }
    /**
     * Get a file or directory.
     *
     * @param localPath: The path to the file.
     *
     * @param options: The options used to fetch the file.
     *
     * @returns A promise which resolves with the file content.
     */
    async get(localPath, options) {
        let model;
        await this._ready;
        if (!this._ydrive.isDir(localPath)) {
            // It's a file.
            return {
                name: new _path__WEBPACK_IMPORTED_MODULE_8__.Path(localPath).name,
                path: localPath,
                type: 'file',
                writable: true,
                created: '',
                last_modified: '',
                mimetype: '',
                content: null,
                format: null
            };
        }
        // It's a directory.
        const content = [];
        const dirContent = this._ydrive.get(localPath);
        for (const [key, value] of dirContent) {
            const isDir = value !== null;
            const type = isDir ? 'directory' : 'file';
            content.push({
                name: key,
                path: `${localPath}/${key}`,
                type,
                writable: true,
                created: '',
                last_modified: '',
                mimetype: '',
                content: null,
                format: null
            });
        }
        model = {
            name: new _path__WEBPACK_IMPORTED_MODULE_8__.Path(localPath).name,
            path: localPath,
            type: 'directory',
            writable: true,
            created: '',
            last_modified: '',
            mimetype: '',
            content,
            format: null
        };
        return model;
    }
    /**
     * Save a file.
     *
     * @param localPath - The desired file path.
     *
     * @param options - Optional overrides to the model.
     *
     * @returns A promise which resolves with the file content model when the
     *   file is saved.
     */
    async save(localPath, options = {}) {
        const fetchOptions = {
            type: options.type,
            format: options.format,
            content: false
        };
        return this.get(localPath, fetchOptions);
    }
}
/**
 * Yjs sharedModel factory for real-time collaboration.
 */
class SharedModelFactory {
    /**
     * Shared model factory constructor
     *
     * @param _onCreate Callback on new document model creation
     */
    constructor(_onCreate) {
        this._onCreate = _onCreate;
        this.documentFactories = new Map();
    }
    /**
     * Register a SharedDocumentFactory.
     *
     * @param type Document type
     * @param factory Document factory
     */
    registerDocumentFactory(type, factory) {
        if (this.documentFactories.has(type)) {
            throw new Error(`The content type ${type} already exists`);
        }
        this.documentFactories.set(type, factory);
    }
    /**
     * Create a new `ISharedDocument` instance.
     *
     * It should return `undefined` if the factory is not able to create a `ISharedDocument`.
     */
    createNew(options) {
        if (typeof options.format !== 'string') {
            console.warn(`Only defined format are supported; got ${options.format}.`);
            return;
        }
        if (this.documentFactories.has(options.contentType)) {
            const sharedModel = this._onCreate(options);
            return sharedModel;
        }
        return;
    }
}


/***/ }),

/***/ "../shared-docprovider/lib/index.js":
/*!******************************************!*\
  !*** ../shared-docprovider/lib/index.js ***!
  \******************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   SharedDrive: () => (/* reexport safe */ _drive__WEBPACK_IMPORTED_MODULE_0__.SharedDrive),
/* harmony export */   WebrtcProvider: () => (/* reexport safe */ _provider__WEBPACK_IMPORTED_MODULE_1__.WebrtcProvider)
/* harmony export */ });
/* harmony import */ var _drive__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./drive */ "../shared-docprovider/lib/drive.js");
/* harmony import */ var _provider__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./provider */ "../shared-docprovider/lib/provider.js");
/* -----------------------------------------------------------------------------
| Copyright (c) Jupyter Development Team.
| Distributed under the terms of the Modified BSD License.
|----------------------------------------------------------------------------*/
/**
 * @packageDocumentation
 * @module shared-docprovider
 */




/***/ }),

/***/ "../shared-docprovider/lib/path.js":
/*!*****************************************!*\
  !*** ../shared-docprovider/lib/path.js ***!
  \*****************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   Path: () => (/* binding */ Path)
/* harmony export */ });
/*
 * Copyright (c) Jupyter Development Team.
 * Distributed under the terms of the Modified BSD License.
 */
class Path {
    constructor(path) {
        this._parts = path.split('/');
        if (this._parts[this._parts.length - 1] === '') {
            this._parts.pop();
        }
    }
    get parts() {
        return this._parts;
    }
    get parent() {
        return this._parts.slice(0, this._parts.length - 1).join('/');
    }
    get name() {
        return this._parts[this._parts.length - 1];
    }
}


/***/ }),

/***/ "../shared-docprovider/lib/provider.js":
/*!*********************************************!*\
  !*** ../shared-docprovider/lib/provider.js ***!
  \*********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   WebrtcProvider: () => (/* binding */ WebrtcProvider)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @lumino/signaling */ "webpack/sharing/consume/default/@lumino/signaling");
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_lumino_signaling__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var y_webrtc__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! y-webrtc */ "webpack/sharing/consume/default/y-webrtc/y-webrtc");
/* harmony import */ var y_webrtc__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(y_webrtc__WEBPACK_IMPORTED_MODULE_3__);
/* -----------------------------------------------------------------------------
| Copyright (c) Jupyter Development Team.
| Distributed under the terms of the Modified BSD License.
|----------------------------------------------------------------------------*/




/**
 * A class to provide Yjs synchronization over WebRTC.
 */
class WebrtcProvider {
    /**
     * Construct a new WebrtcProvider
     *
     * @param options The instantiation options for a WebrtcProvider
     */
    constructor(options) {
        this._onPeers = (event) => {
            if (event.webrtcPeers.length === 0) {
                (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.showErrorMessage)(this._trans.__('All clients disconnected'), `If you close '${this._path}', all data will be lost (unless someone reconnects).`, [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Dialog.okButton()]);
            }
        };
        this._onSync = (synced) => {
            if (synced.synced) {
                this._ready.resolve();
                //this._yWebrtcProvider?.off('status', this._onSync);
            }
        };
        this._ready = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_1__.PromiseDelegate();
        this._isDisposed = false;
        this._path = options.path;
        this._contentType = options.contentType;
        this._format = options.format;
        this._sharedModel = options.model;
        this._awareness = options.model.awareness;
        this._yWebrtcProvider = null;
        this._trans = options.translator;
        this._signalingServers = options.signalingServers;
        const user = options.user;
        user.ready
            .then(() => {
            this._onUserChanged(user);
        })
            .catch(e => console.error(e));
        user.userChanged.connect(this._onUserChanged, this);
        this._connect().catch(e => console.warn(e));
    }
    /**
     * Test whether the object has been disposed.
     */
    get isDisposed() {
        return this._isDisposed;
    }
    /**
     * A promise that resolves when the document provider is ready.
     */
    get ready() {
        return this._ready.promise;
    }
    /**
     * Dispose of the resources held by the object.
     */
    dispose() {
        var _a;
        if (this.isDisposed) {
            return;
        }
        this._isDisposed = true;
        //this._yWebrtcProvider?.off('status', this._onSync);
        (_a = this._yWebrtcProvider) === null || _a === void 0 ? void 0 : _a.destroy();
        _lumino_signaling__WEBPACK_IMPORTED_MODULE_2__.Signal.clearData(this);
    }
    async _connect() {
        this._yWebrtcProvider = new y_webrtc__WEBPACK_IMPORTED_MODULE_3__.WebrtcProvider(`${this._format}:${this._contentType}:${this._path}}`, this._sharedModel.ydoc, {
            signaling: this._signalingServers,
            awareness: this._awareness
        });
        this._yWebrtcProvider.on('synced', this._onSync);
        this._yWebrtcProvider.on('peers', this._onPeers);
    }
    _onUserChanged(user) {
        this._awareness.setLocalStateField('user', user.identity);
    }
}


/***/ }),

/***/ "../shared-docprovider/lib/ydrive.js":
/*!*******************************************!*\
  !*** ../shared-docprovider/lib/ydrive.js ***!
  \*******************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   YDrive: () => (/* binding */ YDrive)
/* harmony export */ });
/* harmony import */ var yjs__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! yjs */ "webpack/sharing/consume/default/yjs");
/* harmony import */ var yjs__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(yjs__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _path__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./path */ "../shared-docprovider/lib/path.js");
/*
 * Copyright (c) Jupyter Development Team.
 * Distributed under the terms of the Modified BSD License.
 */


class YDrive {
    constructor() {
        this._ydoc = new yjs__WEBPACK_IMPORTED_MODULE_0__.Doc();
        this._yroot = this._ydoc.getMap('root');
    }
    get ydoc() {
        return this._ydoc;
    }
    _newDir() {
        return new yjs__WEBPACK_IMPORTED_MODULE_0__.Map();
    }
    isDir(path) {
        return this.get(path) ? true : false;
    }
    get(path) {
        if (path === '') {
            return this._yroot;
        }
        let current = this._yroot;
        const parts = new _path__WEBPACK_IMPORTED_MODULE_1__.Path(path).parts;
        let cwd = '';
        const lastIdx = parts.length - 1;
        for (let idx = 0; idx < parts.length; idx++) {
            const part = parts[idx];
            if (!current.has(part)) {
                throw new Error(`No entry "${part}" in "${cwd}"`);
            }
            current = current.get(part);
            if (current) {
                cwd = cwd === '' ? part : `${cwd}/${part}`;
            }
            else if (idx < lastIdx) {
                throw new Error(`Entry "${part}" in "${cwd}" is not a directory.`);
            }
        }
        return current;
    }
    newUntitled(isDir, path, ext) {
        path = path !== null && path !== void 0 ? path : '';
        ext = ext !== null && ext !== void 0 ? ext : '';
        let idx = 0;
        let newName = '';
        const parent = this.get(path);
        const dir = parent.toJSON();
        while (newName === '') {
            const _newName = `shared${idx}${ext}`;
            if (_newName in dir) {
                idx += 1;
            }
            else {
                newName = _newName;
            }
        }
        const parts = new _path__WEBPACK_IMPORTED_MODULE_1__.Path(path).parts;
        parts.push(newName);
        const newPath = parts.join('/');
        if (isDir) {
            this.createDirectory(newPath);
        }
        else {
            this.createFile(newPath);
        }
        return newPath;
    }
    createFile(path) {
        const parent = this.get(new _path__WEBPACK_IMPORTED_MODULE_1__.Path(path).parent);
        parent.set(new _path__WEBPACK_IMPORTED_MODULE_1__.Path(path).name, null);
    }
    createDirectory(path) {
        const parent = this.get(new _path__WEBPACK_IMPORTED_MODULE_1__.Path(path).parent);
        parent.set(new _path__WEBPACK_IMPORTED_MODULE_1__.Path(path).name, this._newDir());
    }
    delete(path) {
        const parts = new _path__WEBPACK_IMPORTED_MODULE_1__.Path(path).parts;
        if (parts.length === 0) {
            throw new Error('Cannot delete root directory');
        }
        const parent = this.get(new _path__WEBPACK_IMPORTED_MODULE_1__.Path(path).parent);
        parent.delete(new _path__WEBPACK_IMPORTED_MODULE_1__.Path(path).name);
    }
    move(fromPath, toPath) {
        if (new _path__WEBPACK_IMPORTED_MODULE_1__.Path(fromPath).parts.length === 0) {
            throw new Error('Cannot move root directory');
        }
        if (new _path__WEBPACK_IMPORTED_MODULE_1__.Path(toPath).parts.length === 0) {
            throw new Error('Cannot move to root directory');
        }
        const fromParent = this.get(new _path__WEBPACK_IMPORTED_MODULE_1__.Path(fromPath).parent);
        const toParent = this.get(new _path__WEBPACK_IMPORTED_MODULE_1__.Path(toPath).parent);
        const content = fromParent.get(new _path__WEBPACK_IMPORTED_MODULE_1__.Path(fromPath).name).clone();
        this.delete(fromPath);
        toParent.set(new _path__WEBPACK_IMPORTED_MODULE_1__.Path(toPath).name, content);
    }
}


/***/ })

}]);
//# sourceMappingURL=shared-docprovider_lib_index_js.a13e7b0610907b7622b1.js.map