import { HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { ToastrService } from 'ngx-toastr';
import { finalize } from 'rxjs';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss'],
})
export class AppComponent implements OnInit {
  private api: string = 'http://localhost:8000';

  imagePossibleTexts: string[] = [];
  videoPossibleTexts: string[] = [];

  imageUploading: boolean = false;
  imageUploaded: boolean = false;

  videoUploading: boolean = false;
  videoUploaded: boolean = false;

  imagePreviewUrl: string = null!;
  videoPreviewUrl: string = null!;

  constructor(
    private readonly _http: HttpClient,
    private readonly _toastr: ToastrService
  ) {}

  ngOnInit(): void {}

  onImageSelect(event: any) {
    let image = event.target.files[0];

    if (image === null || image === undefined) {
      this._toastr.error('Image does not provided');
      return;
    }

    this.imagePreviewUrl = URL.createObjectURL(image);
    this.imageUploaded = true;

    let formData = this.buildFormData(image);
    this.imageUploading = true;

    this._http
      .post(`${this.api}/upload/image`, formData, {})
      .pipe(
        finalize(() => {
          this.imageUploading = false;
          event.target.value = null;
        })
      )
      .subscribe(({ result }: any) => {
        this.imagePossibleTexts = result;
      });
  }

  onVideoSelect(event: any) {
    let video = event.target.files[0];

    if (video === null || video === undefined) {
      this._toastr.error('Image does not provided');
      return;
    }

    this.videoPreviewUrl = URL.createObjectURL(video);
    this.videoUploaded = true;

    let formData = this.buildFormData(video);
    this.videoUploading = true;

    this._http
      .post(`${this.api}/upload/video`, formData, {})
      .pipe(
        finalize(() => {
          this.videoUploading = false;
          event.target.value = null;
        })
      )
      .subscribe(({ result }: any) => {
        this.videoPossibleTexts = result;
      });
  }

  private buildFormData(file: File) {
    let formData = new FormData();
    formData.append('file', file);
    return formData;
  }
}
