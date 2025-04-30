def add(cls, model, commit=True):
        """Adds a model instance to session and commits the
        transaction.

        Args:

            model: The instance to add.

        Examples:

            >>> customer = Customer.new(name="hari", email="hari@gmail.com")

            >>> Customer.add(customer)
            hari@gmail.com
        """
        if not isinstance(model, cls):
            raise ValueError('%s is not of type %s' % (model, cls))
        cls.session.add(model)
        try:
            if commit:
                cls.session.commit()
            return model
        except:
            cls.session.rollback()
            raise