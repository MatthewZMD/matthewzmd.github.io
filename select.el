;;; select.el --- -*- lexical-binding: t -*-
;;
;; Filename: select.el
;; Description:
;; Author: Mingde (Matthew) Zeng
;; Maintainer:
;; Copyright (C) 2019 Mingde (Matthew) Zeng
;; Created: Fri Nov 24 22:38:59 2023 (-0500)
;; Version:
;; Package-Requires: ()
;; Last-Updated:
;;           By:
;;     Update #: 26
;; URL:
;; Doc URL:
;; Keywords:
;; Compatibility:
;;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;
;;; Commentary:
;;
;;
;;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;
;;; Change Log:
;;
;;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;
;; This program is free software: you can redistribute it and/or modify
;; it under the terms of the GNU General Public License as published by
;; the Free Software Foundation, either version 3 of the License, or (at
;; your option) any later version.
;;
;; This program is distributed in the hope that it will be useful, but
;; WITHOUT ANY WARRANTY; without even the implied warranty of
;; MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
;; General Public License for more details.
;;
;; You should have received a copy of the GNU General Public License
;; along with GNU Emacs.  If not, see <https://www.gnu.org/licenses/>.
;;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;
;;; Code:

(defun eaf-filter-good-photo ()
  "Copy the photo as 'good' to the subdirectory"
  (interactive)
  (let* ((good-directory (expand-file-name "good" default-directory))
         (file-path (eaf-get-path-or-url))
         (file-name (file-name-nondirectory file-path))
         (new-file-path (expand-file-name file-name good-directory)))
    ;; Create 'good' directory if it doesn't exist
    (unless (file-exists-p good-directory)
      (make-directory good-directory))
    ;; Copy the file to the 'good' directory
    (copy-file file-path new-file-path)
    (message "File saved in 'good': %s" new-file-path)))

(eaf-bind-key eaf-filter-good-photo "g" eaf-image-viewer-keybinding)
(eaf-bind-key open_devtools "M-i" eaf-browser-keybinding)
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;; select.el ends here
