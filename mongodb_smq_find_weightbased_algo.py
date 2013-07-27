dbh.smqweight.find({  
"$where":"function()
    {var x = this.TermCategory_I[1].TermWeight;
     var y = this.TermCategory_H[1].TermWeight; 
     var z = this.TermCategory_G[1].TermWeight; 
     if ((x+y+z) > 6) return true;}" 
},{'_id':0})
