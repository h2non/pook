(import [pook])
(import [requests])

(defn request [url &optional [status 404]]
  (doto (.mock pook url) (.reply status))
  (let [res (.get requests url)]
    (. res status_code)))

(defn run []
  (with [(.use pook)]
    (print "Status:" (request "http://foo.com/bar" :status 204))))

;; Run test program
(defmain [&args] (run))
