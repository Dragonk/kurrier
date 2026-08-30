FROM ckulka/baikal:nginx

COPY deploy/images/baikal/entrypoint.sh /usr/local/bin/kurrier-baikal-entrypoint.sh

RUN chmod 0555 /usr/local/bin/kurrier-baikal-entrypoint.sh

ENTRYPOINT ["/usr/local/bin/kurrier-baikal-entrypoint.sh"]
CMD ["nginx", "-g", "daemon off;"]
