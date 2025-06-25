from django.views.generic import TemplateView
from django.http import JsonResponse

class Index(TemplateView):
    template_name = "tictactoe/index.html"
    starting_board = [[' ',' ',' '] for _ in range(3)]
    def init_session(self, req):
        if 'board' not in req.session:
            req.session['board'] = self.starting_board
        if 'won' not in req.session:
            req.session['won'] = False 
        if 'game_over' not in req.session:
            req.session['game_over'] = False 
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['board'] = self.request.session.get('board', self.starting_board) 
        return data
    def get(self, req):
        self.init_session(req)
        ctx = self.get_context_data()
        return self.render_to_response(ctx)
    def post(self,req):
        pass
