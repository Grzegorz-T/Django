$(document).ready(function() {

	$(document).on('click','.btn-outline-warnings', function(event) {
        $.get('/templates/loggin.html')
		req = $.ajax({
            type : 'POST',
			url : '/_login/'
        })
        req.done(function(data) {
            $('.main').append(`
                <div class="container h-100">
                    <div role="dialog" style="bottom: 0px; left: 0px; right: 0px; top: 0px; position: fixed;">
                    <div class="d-flex justify-content-center h-100">
                        <div class="user_card">
                            <div class="d-flex justify-content-center">
                                <h3 id="form-title">LOGIN</h3>
                            </div>
                            <div class="d-flex justify-content-center form_container">
                            
                                <form method="POST" action="">
                                    <div class="input-group mb-3">
                                        <div class="input-group-append">
                                            <span class="input-group-text"><i class="fas fa-user"></i></span>
                                        </div>

                                        <input type="text" name="username" placeholder="Username..." class="form-control">
                                    </div>

                                    <div class="input-group mb-2">
                                        <div class="input-group-append">
                                            <span class="input-group-text"><i class="fas fa-key"></i></span>
                                        </div>

                                            <input type="password" name="password" placeholder="Password..." class="form-control" >
                                    </div>

                                        <div class="d-flex justify-content-center mt-3 login_container">
                                            <input class="btn login_btn" type="submit" value="Login">
                                        </div>
                                </form>

                            </div>

                            {% for message in messagesss %}
                                <p id="messages">{{message}}</p>
                            {% endfor %}			
                    
                            <div class="mt-4">
                                <div class="d-flex justify-content-center links">
                                    Don't have an account? <a href="/register" class="ml-2">Sign Up</a>
                                </div>
                        
                            </div>
                        </div>
                    </div>
                </div>
            `)
        });
    });

});