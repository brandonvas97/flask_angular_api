import { Component, OnInit, ViewChild } from '@angular/core';
import { NgForm } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { ToastrService } from 'ngx-toastr';
import { BookServiceService } from '../book-service.service';

@Component({
  selector: 'app-edit-book',
  templateUrl: './edit-book.component.html',
  styleUrls: ['./edit-book.component.scss']
})
export class EditBookComponent implements OnInit {

  editBookForm: bookForm = new bookForm();

  @ViewChild("bookForm")
  bookForm!: NgForm;

  isSubmitted: boolean = false;
  bookId: any;

  constructor(private toastr: ToastrService, private route: ActivatedRoute, private router: Router,
    private bookService: BookServiceService) { }

  ngOnInit(): void {
    this.bookId = this.route.snapshot.params['bookId'];
    this.getBookById();
  }
  getBookById() {
    this.bookService.listBookById(this.bookId).subscribe((data: any) => {
      if (data != null && data.body != null) {
        var resultData = data.body;
        if (resultData) {
          this.editBookForm.id = resultData.id;
          this.editBookForm.title = resultData.title;
          this.editBookForm.author = resultData.author;
          this.editBookForm.read = resultData.read
        }
      }
    },
      (error: any) => { });
  }

  EditBook(isValid: any) {
    this.isSubmitted = true;
    if (isValid) {
      //console.log("read: ", this.editBookForm.read)
      this.bookService.editBook(this.editBookForm.id, this.editBookForm.title, this.editBookForm.author, this.editBookForm.read).subscribe(async data => {
        if (data != null && data.body != null) {
          var resultData = data.body;
          if (resultData != null) {
            if (resultData != null) {
              this.toastr.success("Book updated successfully");
              setTimeout(() => {
                this.router.navigate(['/']);
              }, 500);
            }
          }
        }
      },
        async error => {
          this.toastr.error("Error when trying to update the book");
          setTimeout(() => {
            this.router.navigate(['/']);
          }, 500);
        });
    }
  }

}

export class bookForm {
  id:any;
  title:any;
  author:any;
  read:boolean;

  constructor(data?: Partial<bookForm>) {
    this.id = data?.id || '';
    this.title = data?.title || '';
    this.author = data?.author || '';
    this.read = data?.read === true; // Ensure read is always a boolean
  }
}
