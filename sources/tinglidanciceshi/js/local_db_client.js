(function() {
    function LocalQuery(client, table) {
        this.client = client;
        this.table = table;
        this.action = null;
        this.selectExpr = '*';
        this.filters = [];
        this.orderBy = null;
        this.limitCount = null;
        this.singleRow = false;
        this.payloadData = null;
    }

    LocalQuery.prototype.select = function(expr) {
        this.action = 'select';
        this.selectExpr = expr || '*';
        return this;
    };

    LocalQuery.prototype.eq = function(column, value) {
        this.filters.push({ column: column, operator: 'eq', value: value });
        return this;
    };

    LocalQuery.prototype.order = function(column, options) {
        options = options || {};
        this.orderBy = { column: column, ascending: options.ascending !== false };
        return this;
    };

    LocalQuery.prototype.limit = function(count) {
        this.limitCount = count;
        return this;
    };

    LocalQuery.prototype.single = function() {
        this.singleRow = true;
        return this.execute();
    };

    LocalQuery.prototype.insert = function(data) {
        this.action = 'insert';
        this.payloadData = data;
        return this.execute();
    };

    LocalQuery.prototype.update = function(data) {
        this.action = 'update';
        this.payloadData = data;
        return this;
    };

    LocalQuery.prototype.then = function(resolve, reject) {
        return this.execute().then(resolve, reject);
    };

    LocalQuery.prototype.catch = function(reject) {
        return this.execute().catch(reject);
    };

    LocalQuery.prototype.execute = async function() {
        var body = {
            table: this.table,
            action: this.action || 'select',
            select: this.selectExpr,
            filters: this.filters,
            order: this.orderBy,
            limit: this.limitCount,
            single: this.singleRow,
            data: this.payloadData
        };
        try {
            var response = await fetch(this.client.endpoint, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(body)
            });
            var result = await response.json();
            if (!response.ok && !result.error) {
                result.error = { message: '本地数据库请求失败：' + response.status };
            }
            return result;
        } catch (e) {
            return { data: null, error: { message: e.message || String(e) } };
        }
    };

    function LocalDbClient(endpoint) {
        this.endpoint = endpoint || '/api/db';
    }

    LocalDbClient.prototype.from = function(table) {
        return new LocalQuery(this, table);
    };

    window.createLocalDbClient = function(endpoint) {
        return new LocalDbClient(endpoint);
    };
})();
