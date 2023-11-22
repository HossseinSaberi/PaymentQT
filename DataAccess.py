from Utils import ReadEnvFile
from psycopg2 import extras, connect


class GetDBVar:
    def __init__(self):
        self.env_file = ReadEnvFile()

    def get_host(self):
        return self.get_key('HOST')

    def get_port(self):
        return self.get_key('PORT')

    def get_username(self):
        return self.get_key('USERRNAME')

    def get_pass(self):
        return self.get_key('PASSWORD')

    def get_dbname(self):
        return self.get_key('DB_NAME')

    def get_key(self, key_name):
        return self.env_file.get_env(key_name)


class ConnectToDB:
    def __init__(self):
        self.db_var = GetDBVar()
        self.conn = None

    def create_conn(self):
        self.conn = connect(user=self.db_var.get_username(), password=self.db_var.get_pass(),
                            host=self.db_var.get_host(), port=self.db_var.get_port(),
                            database=self.db_var.get_dbname())
        self.conn.autocommit = True

    def get_conn(self):
        if not self.conn:
            self.create_conn()
        return self.conn

    def conn_close(self):
        self.conn.close()


class InitDB:
    def __init__(self, db_connection):
        self.db_conn = db_connection
        self.init_db()

    def init_db(self):
        self.initial_functions()
        self.initial_types()
        self.create_user_table()
        self.create_payment_table()
        self.create_installment_table()

    def create_user_table(self):
        cursor = self.db_conn.cursor()
        query = """
            DROP TABLE IF EXISTS public.users;
            CREATE TABLE public.users (
            full_name text NOT NULL,
            phone_number text NOT NULL,
            address text NOT NULL,
            description text NOT NULL DEFAULT ' - '::text,,
            uid serial4 NOT NULL,
            user_type public.valid_user_type NOT NULL,
            CONSTRAINT users_pk PRIMARY KEY (uid)
            );
        """
        cursor.execute(query)

    def create_payment_table(self):
        cursor = self.db_conn.cursor()
        query = """
            DROP TABLE IF EXISTS public.payments;
            CREATE TABLE public.payments (
                pid serial4 NOT NULL,
                user_id int4 NOT NULL,
                total_price int8 NOT NULL,
                last_update timestamp NOT NULL,
                first_date timestamp NOT NULL,
                remainder int8 NOT NULL,
                paied int8 NOT NULL,
                installment int8 NOT NULL,
                status text NOT NULL,
                CONSTRAINT payments_pk PRIMARY KEY (pid)
            );
            create trigger update_last_update before
            update
                on
                public.payments for each row execute function last_update();
            create trigger set_first_date before
            insert
                on
                public.payments for each row execute function first_insert();
            ALTER TABLE public.payments ADD CONSTRAINT payments_fk FOREIGN KEY (user_id) REFERENCES public.users(uid) ON DELETE CASCADE;
            """
        cursor.execute(query)

    def create_salary_table(self):
        cursor = self.db_conn.cursor()
        query = """
        DROP TABLE IF EXISTS public.salary;
        CREATE TABLE public.salary (
            office_id int4 NOT NULL,
            total_money int8 NOT NULL,
            sid serial4 NOT NULL,
            first_date timestamp NULL,
            description text NOT NULL DEFAULT ' - '::text,
            CONSTRAINT salary_pk PRIMARY KEY (sid)
        );
        create trigger set_first_date before
        insert
            on
            public.salary for each row execute function first_insert();
    """
        cursor.execute(query)

    def create_installment_table(self):
        cursor = self.db_conn.cursor()
        query = """
        DROP TABLE IF EXISTS public.installment;
        
        CREATE TABLE public.installment (
            office_id int4 NOT NULL,
            total_money  int8 NOT NULL,
            installment_money int8 NOT NULL,
            remainder_money int8 NOT NULL DEFAULT 0,
            inid serial4 NOT NULL,
            last_update timestamp NULL,
            first_date timestamp NULL,
            start_date text NOT NULL,
            description text NOT NULL DEFAULT ' - '::text,
            CONSTRAINT payments_pk PRIMARY KEY (inid)
        );
        
        -- Table Triggers
        
        create trigger update_last_update before
        update
            on
            public.installment for each row execute function last_update();
        create trigger set_first_date before
        insert
            on
            public.installment for each row execute function first_insert();
    """
        cursor.execute(query)

    def initial_types(self):
        self.user_type()

    def initial_functions(self):
        self.first_insert_creation()
        self.last_update_creation()

    def user_type(self):
        cursor = self.db_conn.cursor()
        query = """
            CREATE TYPE public.valid_user_type AS ENUM (
                'شخص',
                'موسسه',
                'ثابت');
          """
        cursor.execute(query)

    def first_insert_creation(self):
        cursor = self.db_conn.cursor()
        query = """
            CREATE OR REPLACE FUNCTION public.first_insert()
            RETURNS trigger
            LANGUAGE plpgsql
            AS $function$
            BEGIN
                NEW.first_date = NOW();
                RETURN NEW;
            END;
            $function$;
        """
        cursor.execute(query)

    def last_update_creation(self):
        cursor = self.db_conn.cursor()
        query = """
                CREATE OR REPLACE FUNCTION public.last_update()
                RETURNS trigger
                LANGUAGE plpgsql
                AS $function$
                BEGIN
                    NEW.last_update = NOW();
                    RETURN NEW;
                END;
                $function$;
        """
        cursor.execute(query)


class Queries:
    def __init__(self, db_connection):
        self.db_conn = db_connection

    def get_user_list(self, type_filter=None):
        with self.db_conn.cursor() as cursor:
            additional_query = ";" if not type_filter else " WHERE user_type = '{}';".format(type_filter)
            query = """
                        SELECT  uid , full_name  FROM users
                     """
            query += additional_query
            cursor.execute(query)
            result = cursor.fetchall()
        return result

    def insert_new_user(self, user_details: dict):
        with self.db_conn.cursor() as cursor:
            try:
                query = """
                         INSERT INTO public.users
                         (full_name,phone_number, address, description , user_type)
                         VALUES
                         ('{}','{}','{}','{}','{}')
                         """.format(
                    user_details['name'], user_details['phone_number'], user_details['address'],
                    user_details['description'], user_details['type'])
                cursor.execute(query)
            except Exception as e:
                print(e)

    def insert_new_payment(self, payment_details: dict):
        with self.db_conn.cursor() as cursor:
            query = """
                INSERT INTO public.payments
                (user_id, total_price, remainder, paied, description, status)
                VALUES
                ({},{},{},{},'{}','{}')""".format(payment_details['user_id'], payment_details['total_money'],
                                                  payment_details['remainder'], payment_details['paied_money'],
                                                  payment_details['description'], payment_details['status'])
            cursor.execute(query)

    def insert_new_isntallment(self, installment_details: dict):
        with self.db_conn.cursor() as cursor:
            try:
                query = """
                    INSERT INTO public.installment
                    (office_id, total_money, installment_money, start_date,description)
                    VALUES
                    ({},{},{},'{}','{}')""".format(installment_details['office_id'], installment_details['total_money'],
                                                   installment_details['installment'], installment_details['start_date'],
                                                   installment_details['description'])
                cursor.execute(query)
            except Exception as e:
                print(e)

    def insert_new_salary(self, salary_details: dict):
        with self.db_conn.cursor() as cursor:
            try:
                query = """
                    INSERT INTO public.salary
                    (office_id, total_money,description)
                    VALUES
                    ({},{},'{}')""".format(salary_details['office_id'], salary_details['total_money'],
                                                   salary_details['description'])
                cursor.execute(query)
            except Exception as e:
                print(e)

    def get_debtor_creditor_list(self, status):
        with self.db_conn.cursor(cursor_factory=extras.DictCursor) as cursor:
            query = """
                SELECT p.pid, u.full_name , p.total_price , p.paied , p.remainder , p.first_date , p.last_update , p.description FROM payments p 
                INNER JOIN users u
                ON
                p.user_id = u.uid
                WHERE p.status = '{}'
            """.format(status)
            cursor.execute(query)
            result = cursor.fetchall()
            return result

    def get_installment_list(self):
        with self.db_conn.cursor(cursor_factory=extras.DictCursor) as cursor:
            query = """
                SELECT i.inid, u.full_name, i.total_money , i.installment_money , i.remainder_money , i.start_date ,i.last_update , i.description FROM installment i 
                INNER JOIN users u
                ON
                i.office_id = u.uid
            """
            cursor.execute(query)
            result = cursor.fetchall()
            return result

    def get_salary_list(self):
        with self.db_conn.cursor(cursor_factory=extras.DictCursor) as cursor:
            query = """
                SELECT s.sid, u.full_name, s.total_money, s.first_date ,  s.description FROM salary s 
                INNER JOIN users u
                ON
                s.office_id = u.uid
            """
            cursor.execute(query)
            result = cursor.fetchall()
            return result


if __name__ == '__main__':
    # x = DataAccess()
    # x.initial_db()
    #
    db_conn = ConnectToDB()
    db_creation = InitDB(db_conn.get_conn())
    db_conn.conn_close()
    #
